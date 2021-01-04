module Reaction_Sandbox_bioTH_class

#include "petsc/finclude/petscsys.h"
  use petscsys
  use Reaction_Sandbox_Base_class
  use Global_Aux_module
  use Reactive_Transport_Aux_module
  use PFLOTRAN_Constants_module

  implicit none
  
  private

  type, public, &
    extends(reaction_sandbox_base_type) :: reaction_sandbox_bioTH_type
    
    PetscInt :: species_Vaq_id ! Aqueous species
    PetscInt :: species_Vim_id ! Immobile species  
    
    !Name of bioparticle species
    character(len=MAXWORDLENGTH) :: name_aqueous
    character(len=MAXWORDLENGTH) :: name_immobile
    
    !Decay rates (Temperature model)
    PetscReal :: logDref_aqueous
    PetscReal :: Tref_aqueous
    PetscReal :: zT_aqueous
    PetscReal :: nAq_aqueous

    !Decay rates (Constant)
    PetscReal :: decay_adsorbed
    
    !Attachment/detachment rates
    PetscReal :: rate_attachment
    PetscReal :: rate_detachment
    
    !Zero concentration (low boundary)
    PetscReal :: zero_concentration

  contains
    procedure, public :: ReadInput => bioTH_Read
    procedure, public :: Setup => bioTH_Setup
    procedure, public :: Evaluate => bioTH_React
    procedure, public :: Destroy => bioTH_Destroy
  
  end type reaction_sandbox_bioTH_type

  public :: bioTH_Create

contains

! ************************************************************************** !

function bioTH_Create()
  ! 
  ! Allocates particle transport variables.
  ! 
  ! Author: Edwin Saavedra C
  ! Date: 09/04/2020
  ! 

  implicit none
  
  class(reaction_sandbox_bioTH_type), pointer :: bioTH_Create
  
  allocate(bioTH_Create)
  bioTH_Create%species_Vaq_id = 0
  bioTH_Create%species_Vim_id = 0

  bioTH_Create%name_aqueous = ''
  bioTH_Create%name_immobile = ''

  bioTH_Create%logDref_aqueous = 0.d0
  bioTH_Create%Tref_aqueous = 0.d0
  bioTH_Create%zT_aqueous = 0.d0
  bioTH_Create%nAq_aqueous = 0.d0

  bioTH_Create%decay_adsorbed = 0.d0
  bioTH_Create%rate_attachment = 0.d0
  bioTH_Create%rate_detachment = 0.d0

  bioTH_Create%zero_concentration = 0.d0

  nullify(bioTH_Create%next)

  PRINT *, "Allocation done" ! Edwin debugging    

end function bioTH_Create

! ************************************************************************** !

subroutine bioTH_Read(this,input,option)
  ! 
  ! Reads input deck for reaction sandbox parameters
  ! 
  ! Author: Edwin
  ! Date: 09/04/2020
  ! 
  use Option_module
  use String_module
  use Input_Aux_module
  use Utility_module
  use Units_module, only : UnitsConvertToInternal
  
  implicit none

  class(reaction_sandbox_bioTH_type) :: this
  type(input_type), pointer :: input
  type(option_type) :: option

  character(len=MAXWORDLENGTH) :: word, internal_units
!  type(particle_type), pointer :: new_particle, prev_particle
 
!  nullify(new_particle)
!  nullify(prev_particle)

call InputPushBlock(input,option)
  do 
    call InputReadPflotranString(input,option)
    if (InputError(input)) exit
    if (InputCheckExit(input,option)) exit

    call InputReadCard(input,option,word)
    call InputErrorMsg(input,option,'keyword', &
                       'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP')
    call StringToUpper(word)   

    select case(trim(word))
      ! Bioparticle name while in suspension
      case('PARTICLE_NAME_AQ')
        call InputReadWord(input,option,this%name_aqueous,PETSC_TRUE)  
        call InputErrorMsg(input,option,'name_aqueous', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,NAMEAQ')
        PRINT *, "Read particles' aq name: ", this%name_aqueous ! Edwin debugging    
      
      ! Bioparticle name while immobilized
      case('PARTICLE_NAME_IM')
        call InputReadWord(input,option,this%name_immobile,PETSC_TRUE)  
        call InputErrorMsg(input,option,'name_immobile', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,NAMEIM')
        PRINT *, "Read particles' immobile name: ", this%name_immobile ! Edwin debugging    

      ! Attachment rate   
      case('RATE_ATTACHMENT')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%rate_attachment)
        call InputErrorMsg(input,option,'rate_attachment', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,Katt')
        PRINT *, "Read attachment rate: ", this%rate_attachment ! Edwin debugging    
        PRINT "(ES12.4)",this%rate_attachment

        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTEMP,RATE CONSTANT UNITS'
          call InputDefaultMsg(input,option)
        else              
          ! If units exist, convert to internal units of 1/s
          internal_units = 'unitless/sec'
          this%rate_attachment = this%rate_attachment * &
            UnitsConvertToInternal(word,internal_units,option)
        endif

      ! Detachment rate   
      case('RATE_DETACHMENT')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%rate_detachment)
        call InputErrorMsg(input,option,'rate_detachment', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,kdet')
        PRINT *, "Read detachment rate: " ! Edwin debugging    
        PRINT "(ES12.4)", this%rate_detachment

        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTEMP,RATE CONSTANT UNITS'
          call InputDefaultMsg(input,option)
        else              
          ! If units exist, convert to internal units of 1/s
          internal_units = 'unitless/sec'
          this%rate_detachment = this%rate_detachment * &
            UnitsConvertToInternal(word,internal_units,option)
        endif      

      ! Decay while in aqueous suspension rate  
      !! **MODEL from Temp**
      case('DECAY_AQ_MODEL')
!!!!!!!!!!!!!!!!!!!!!!!!111111
        call InputPushBlock(input,option)
        do
          call InputReadPflotranString(input,option)
          if (InputError(input)) exit
          if (InputCheckExit(input,option)) exit

          call InputReadCard(input,option,word)
          call InputErrorMsg(input,option,'keyword', &
                       'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,DECAY_AQ_MODEL')
          call StringToUpper(word)

          select case(trim(word))
          ! Reference temperature (Probably 4°C)  
          case('TREF')
            call InputReadDouble(input,option,this%Tref_aqueous)
            call InputErrorMsg(input,option,'TrefAq', &
                        'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,DECAY_AQ_MODEL,TREF')
            PRINT *, "Read Tref for decay aqueous model: " 
            PRINT "(ES12.4)", this%Tref_aqueous ! Edwin debugging 
          
          ! Model parameter zT  
          case('ZT')
            call InputReadDouble(input,option,this%zT_aqueous)
            call InputErrorMsg(input,option,'decay_aqueous_zT', &
                        'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,DECAY_AQ_MODEL,ZT')
            PRINT *, "zT parameter: "  ! Edwin debugging   
            PRINT "(ES12.4)", this%zT_aqueous

          ! Model parameter n (Probably 2.0)  
          case('N')
            call InputReadDouble(input,option,this%nAq_aqueous)
            call InputErrorMsg(input,option,'decay_aqueous_nAq', &
                        'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMPDECAY_AQ_MODEL,N')
            PRINT *, "n parameter: " ! Edwin debugging   
            PRINT "(ES12.4)", this%nAq_aqueous

          ! D reference value (Probably 2.3)  
          case('LOGDREF')
            call InputReadDouble(input,option,this%logDref_aqueous)
            call InputErrorMsg(input,option,'decay_aqueous_logDref', &
                        'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMPDECAY_AQ_MODEL,LOGDREF')
            PRINT *, "log(D_ref) parameter: " ! Edwin debugging 
            PRINT "(ES12.4)", this%logDref_aqueous

          ! Something else
          case default
            call InputKeywordUnrecognized(input,word, &
                   'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,DECAY_AQ_MODEL',option)
          end select
        enddo
      call InputPopBlock(input,option)
      ! Decay while immobilized (adsorbed)   
      case('DECAY_ADSORBED')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%decay_adsorbed)
        call InputErrorMsg(input,option,'decay_adsorbed', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,DECAY_ADSORBED')
        PRINT *, "Read decay while adsorbed rate: "   
        PRINT "(ES12.4)", this%decay_adsorbed ! Edwin debugging 
        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTEMP,RATE CONSTANT UNITS'
          call InputDefaultMsg(input,option)
        else              
          ! If units exist, convert to internal units of 1/s
          internal_units = 'unitless/sec'
          this%decay_adsorbed = this%decay_adsorbed * &
            UnitsConvertToInternal(word,internal_units,option)
        endif

        ! Zero concentration for log calculation
        ! for instance, assume 1E-35 is a just 0.0 mol/L
      case('ZERO_CONCENTRATION')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%zero_concentration)
        call InputErrorMsg(input,option,'zero_concentration', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP,zeroConcentration')
        PRINT *, "Read zero concentration value: "
        PRINT "(ES12.4)", this%zero_concentration ! Edwin debugging    
        ! Default break if nothing found in sandbox
      case default
        call InputKeywordUnrecognized(input,word, &
                     'CHEMISTRY,REACTION_SANDBOX,BIOPARTEMP',option)
    end select
  enddo
  call InputPopBlock(input,option)
  
  PRINT *, "Conf. file block ended" ! Edwin debugging    
end subroutine bioTH_Read

subroutine bioTH_Setup(this,reaction,option)
  ! 
  ! Sets up the kinetic attachment/dettachment reactions
  ! 
  ! Author: Edwin
  ! Date: 04/09/2020
  ! 

  use Reaction_Aux_module, only : reaction_rt_type, GetPrimarySpeciesIDFromName
  use Reaction_Immobile_Aux_module, only : GetImmobileSpeciesIDFromName
  use Option_module

  implicit none
  
  class(reaction_sandbox_bioTH_type) :: this
  class(reaction_rt_type) :: reaction
  type(option_type) :: option
  
  PRINT *, "Entered the Setup block :o" ! Edwin debugging 
  
  ! 9. Add code to initialize 
  this%species_Vaq_id = &
    GetPrimarySpeciesIDFromName(this%name_aqueous,reaction,option)
  PRINT *, "Found name of aqueous species" ! Edwin debugging    

  this%species_Vim_id = &
    GetImmobileSpeciesIDFromName(this%name_immobile,reaction%immobile,option)
  PRINT *, "Found name of immobile species" ! Edwin debugging 

end subroutine bioTH_Setup

subroutine bioTH_React(this,Residual,Jacobian,compute_derivative, &
                        rt_auxvar,global_auxvar,material_auxvar, &
                        reaction, option)
  ! 
  ! Evaluates reaction
  ! 
  ! Author: Edwin
  ! Date: 04/09/2020
  ! 
  
  use Option_module
  use String_module
  use Reaction_Aux_module, only : reaction_rt_type
  use Reaction_Immobile_Aux_module
  use Material_Aux_class, only : material_auxvar_type

  implicit none

  class(reaction_sandbox_bioTH_type) :: this  
  type(option_type) :: option
  class(reaction_rt_type) :: reaction
  PetscBool :: compute_derivative
  
  ! the following arrays must be declared after reaction
  PetscReal :: Residual(reaction%ncomp)
  PetscReal :: Jacobian(reaction%ncomp,reaction%ncomp)
  type(reactive_transport_auxvar_type) :: rt_auxvar
  type(global_auxvar_type) :: global_auxvar
  class(material_auxvar_type) :: material_auxvar

  PetscInt, parameter :: iphase = 1
  PetscReal :: volume                 ! m^3 bulk
  PetscReal :: porosity               ! m^3 pore space / m^3 bulk
  PetscReal :: liquid_saturation      ! m^3 water / m^3 pore space
  PetscReal :: L_water                ! L water

  PetscReal :: Vaq  ! mol/L
  PetscReal :: Vim  ! mol/m^3
  PetscReal :: Rate
  PetscReal :: RateAtt, RateDet  ! mol/sec
  PetscReal :: RateDecayAq, RateDecayIm !Check units
  PetscReal :: stoichVaq
  PetscReal :: stoichVim
  PetscReal :: katt, kdet
  PetscReal :: decayAq, decayIm
  PetscReal :: temperature
  PetscReal :: ZeroConc

  ! Decay model parameters
  PetscReal :: logDrefAq
  PetscReal :: TrefAq
  PetscReal :: zTAq
  PetscReal :: nAq

  porosity = material_auxvar%porosity
  liquid_saturation = global_auxvar%sat(iphase)
  volume = material_auxvar%volume
  L_water = porosity*liquid_saturation*volume*1.d3  ! 1.d3 converts m^3 water -> L water
  temperature = global_auxvar%temp

  ! Add a pseudo-zero to concentrations
  ZeroConc = this%zero_concentration

! Assign concentrations of Vaq and Vim
  Vaq = rt_auxvar%total(this%species_Vaq_id,iphase) - ZeroConc
  Vim = rt_auxvar%immobile(this%species_Vim_id) - ZeroConc
!  PRINT *, "Assigned Vaq/Vim concentrations" ! Edwin debugging    

  ! initialize all rates to zero
  Rate = 0.d0
  RateAtt = 0.d0
  RateDet = 0.d0
  RateDecayAq = 0.d0
  RateDecayIm = 0.d0
  
  ! stoichiometries
  ! reactants have negative stoichiometry
  ! products have positive stoichiometry
  stoichVaq = -1.d0
  stoichVim = 1.d0

  ! kinetic rate constants
  katt = 0.d0
  kdet = 0.d0
  katt = this%rate_attachment
  kdet = this%rate_detachment  
  !  PRINT *, "Assigned attachment/detachment rates" ! Edwin debugging    

  ! decay(temperature dependent) rates
  ! Check Guillier et al. for model equation (2020)
  !  decay = ln(10)/D
  !  logD = logDref - [(T-Tref)/zT]^n

  logDrefAq = 0.0
  TrefAq = 0.0
  zTAq = 0.0
  nAq = 0.0

  logDrefAq = this%logDref_aqueous
  TrefAq = this%Tref_aqueous
  zTAq = this%zT_aqueous
  nAq = this%nAq_aqueous

  
  decayAq = (2.302585/(10.0 ** (logDrefAq - (((temperature - TrefAq)/zTAq)**nAq))))/3600  ! 1/s
  ! PRINT *, "Temperature:"
  ! PRINT "(ES12.4)", temperature
  ! PRINT *, "Decay Rate 1/s:"
  ! PRINT "(ES12.4)", decayAq !(Should be 4.45E-6 for a 10°C)

  decayIm = this%decay_adsorbed
!  PRINT *, "Assigned decay rates" ! Edwin debugging    

  RateAtt = 0.0
  RateDet = 0.0
  RateDecayAq = 0.0
  RateDecayIm = 0.0

  
  ! Build here for attachment/detachment
  ! first-order forward - reverse (A <-> C)
  Rate = katt * Vaq * L_water - kdet * Vim * volume
  RateAtt = stoichVaq * Rate
  RateDet = stoichVim * Rate

  ! Build here for inactivation reactions
  ! first-order (A -> X)
  Rate = decayAq * Vaq * L_water
  RateDecayAq = - Rate 

  Rate = decayIm * Vim * volume
  RateDecayIm = - Rate 

  IF ( Vaq > 0.0 ) THEN
    IF ( Vim > 0.0 ) THEN
      !PRINT *, "AQ > 0 and IM > 0"
      Residual(this%species_Vaq_id) = &
        Residual(this%species_Vaq_id) - RateAtt - RateDecayAq
  
      Residual(this%species_Vim_id + reaction%offset_immobile) = &
        Residual(this%species_Vim_id + reaction%offset_immobile) &
        - RateDet - RateDecayIm

    ELSE IF ( Vim <= 0.0 ) THEN
      !PRINT *, "AQ > 0 but IM < 0"
      Vim = ZeroConc
      RateDet = 0.0
      RateDecayIm = 0.0

      Residual(this%species_Vaq_id) = &
        Residual(this%species_Vaq_id) - RateAtt - RateDecayAq
  
      Residual(this%species_Vim_id + reaction%offset_immobile) = &
        Residual(this%species_Vim_id + reaction%offset_immobile) &
        - RateDet - RateDecayIm
      
    END IF
  ELSE IF ( Vaq <= 0.0 ) THEN
    IF ( Vim > 0.0 ) THEN
      !PRINT *, "AQ < 0 but IM > 0"
      Vaq = ZeroConc
      RateAtt = 0.0
      RateDecayAq = 0.0
  
      Residual(this%species_Vaq_id) = &
        Residual(this%species_Vaq_id) - RateAtt - RateDecayAq
  
      Residual(this%species_Vim_id + reaction%offset_immobile) = &
        Residual(this%species_Vim_id + reaction%offset_immobile) &
        - RateDet - RateDecayIm
  
    ELSE IF ( Vim <= 0.0 ) THEN
      !PRINT *, "AQ < 0 and IM < 0"
      Vim = ZeroConc
      Vaq = ZeroConc
      RateAtt = 0.0
      RateDet = 0.0
      RateDecayAq = 0.0
      RateDecayIm = 0.0

      Residual(this%species_Vaq_id) = &
        Residual(this%species_Vaq_id) - RateAtt - RateDecayAq

      Residual(this%species_Vim_id + reaction%offset_immobile) = &
        Residual(this%species_Vim_id + reaction%offset_immobile) &
        - RateDet - RateDecayIm
    END IF
  END IF
  
  ! NOTES
  ! 1. Always subtract contribution from residual
  ! 2. Units of residual are moles/second  
  ! Residual(this%species_Vaq_id) = &
  !   Residual(this%species_Vaq_id) - RateAtt - RateDecayAq
  
  ! Residual(this%species_Vim_id + reaction%offset_immobile) = &
  !   Residual(this%species_Vim_id + reaction%offset_immobile) &
  !   - RateDet - RateDecayIm

end subroutine bioTH_React

subroutine bioTH_Destroy(this)
  ! 
  ! Destroys allocatable or pointer objects created in this
  ! module
  ! 
  ! Author: John Doe
  ! Date: 00/00/00
  ! 

  implicit none
  
  class(reaction_sandbox_bioTH_type) :: this  

! 12. Add code to deallocate contents of the example object

end subroutine bioTH_Destroy

end module Reaction_Sandbox_bioTH_class

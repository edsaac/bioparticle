module Reaction_Sandbox_escPTr_class

#include "petsc/finclude/petscsys.h"
  use petscsys
  use Reaction_Sandbox_Base_class
  use Global_Aux_module
  use Reactive_Transport_Aux_module
  use PFLOTRAN_Constants_module

  implicit none
  
  private

  type, public, &
    extends(reaction_sandbox_base_type) :: reaction_sandbox_escPTr_type
    
    PetscInt :: species_Vaq_id ! Aqueous species
    PetscInt :: species_Vim_id ! Immobile species  
    
    !Name of bioparticle species
    character(len=MAXWORDLENGTH) :: name_aqueous
    character(len=MAXWORDLENGTH) :: name_immobile
    
    !Decay rates
    PetscReal :: decay_aqueous
    PetscReal :: decay_adsorbed
    
    !Attachment/detachment rates
    PetscReal :: rate_attachment
    PetscReal :: rate_detachment
      
  contains
    procedure, public :: ReadInput => escPTr_Read
    procedure, public :: Setup => escPTr_Setup
    procedure, public :: Evaluate => escPTr_React
    procedure, public :: Destroy => escPTr_Destroy
  
  end type reaction_sandbox_escPTr_type

  public :: escPTr_Create

contains

! ************************************************************************** !

function escPTr_Create()
  ! 
  ! Allocates particle transport variables.
  ! 
  ! Author: Edwin Saavedra C
  ! Date: 09/04/2020
  ! 

  implicit none
  
  class(reaction_sandbox_escPTr_type), pointer :: escPTr_Create
  
  allocate(escPTr_Create)
  escPTr_Create%species_Vaq_id = 0
  escPTr_Create%species_Vim_id = 0

  escPTr_Create%name_aqueous = ''
  escPTr_Create%name_immobile = ''

  escPTr_Create%decay_aqueous = 0.d0
  escPTr_Create%decay_adsorbed = 0.d0
  escPTr_Create%rate_attachment = 0.d0
  escPTr_Create%rate_detachment = 0.d0

  PRINT *, "Allocation done" ! Edwin debugging    

end function escPTr_Create

! ************************************************************************** !

subroutine escPTr_Read(this,input,option)
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

  class(reaction_sandbox_escPTr_type) :: this
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
                       'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE')
    call StringToUpper(word)   

    select case(trim(word))
      ! Bioparticle name while in suspension
      case('PARTICLE_NAME_AQ')
        call InputReadWord(input,option,this%name_aqueous,PETSC_TRUE)  
        call InputErrorMsg(input,option,'name_aqueous', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE,NAMEAQ')
        PRINT *, "Read particles' aq name" ! Edwin debugging    
      
      ! Bioparticle name while immobilized
      case('PARTICLE_NAME_IM')
        call InputReadWord(input,option,this%name_immobile,PETSC_TRUE)  
        call InputErrorMsg(input,option,'name_immobile', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE,NAMEIM')
        PRINT *, "Read particles' immobile name" ! Edwin debugging    
      ! Attachment rate   
      case('RATE_ATTACHMENT')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%rate_attachment)
        call InputErrorMsg(input,option,'rate_attachment', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE,Katt')
        PRINT *, "Read attachment rate" ! Edwin debugging    
        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTICLE,RATE CONSTANT UNITS'
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
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE,kdet')
        PRINT *, "Read detachment rate" ! Edwin debugging    
        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTICLE,RATE CONSTANT UNITS'
          call InputDefaultMsg(input,option)
        else              
          ! If units exist, convert to internal units of 1/s
          internal_units = 'unitless/sec'
          this%rate_detachment = this%rate_detachment * &
            UnitsConvertToInternal(word,internal_units,option)
        endif

      ! Decay while in aqueous suspension rate   
      case('DECAY_AQUEOUS')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%decay_aqueous)
        call InputErrorMsg(input,option,'decay_aqueous', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE,decayAq')
        PRINT *, "Read decay aqueous phase rate" ! Edwin debugging    
        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTICLE,RATE CONSTANT UNITS'
          call InputDefaultMsg(input,option)
        else              
          ! If units exist, convert to internal units of 1/s
          internal_units = 'unitless/sec'
          this%decay_aqueous = this%decay_aqueous * &
            UnitsConvertToInternal(word,internal_units,option)
        endif

      ! Decay while immobilized (adsorbed)   
      case('DECAY_ADSORBED')
        ! Read the double precision rate constant
        call InputReadDouble(input,option,this%decay_adsorbed)
        call InputErrorMsg(input,option,'decay_adsorbed', &
                           'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE,decayIm')
        PRINT *, "Read decay while adsorbed rate" ! Edwin debugging    
        ! Read the units
        call InputReadWord(input,option,word,PETSC_TRUE)
        if (InputError(input)) then
          ! If units do not exist, assume default units of 1/s which are the
          ! standard internal PFLOTRAN units for this rate constant.
          input%err_buf = 'REACTION_SANDBOX,BIOPARTICLE,RATE CONSTANT UNITS'
          call InputDefaultMsg(input,option)
        else              
          ! If units exist, convert to internal units of 1/s
          internal_units = 'unitless/sec'
          this%decay_adsorbed = this%decay_adsorbed * &
            UnitsConvertToInternal(word,internal_units,option)
        endif
      case default
        call InputKeywordUnrecognized(input,word, &
                     'CHEMISTRY,REACTION_SANDBOX,BIOPARTICLE',option)
    end select
  enddo
  call InputPopBlock(input,option)
  
  PRINT *, "Conf. file block ended" ! Edwin debugging    
end subroutine escPTr_Read

subroutine escPTr_Setup(this,reaction,option)
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
  
  class(reaction_sandbox_escPTr_type) :: this
  class(reaction_rt_type) :: reaction
  type(option_type) :: option

  ! 9. Add code to initialize 
  this%species_Vaq_id = &
    GetPrimarySpeciesIDFromName(this%name_aqueous,reaction,option)
  PRINT *, "Found name of aqueous species" ! Edwin debugging    

  this%species_Vim_id = &
    GetImmobileSpeciesIDFromName(this%name_immobile,reaction%immobile,option)
  PRINT *, "Found name of immobile species" ! Edwin debugging    

end subroutine escPTr_Setup

subroutine escPTr_React(this,Residual,Jacobian,compute_derivative, &
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

  class(reaction_sandbox_escPTr_type) :: this  
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
  PetscReal :: stoichVaq
  PetscReal :: stoichVim
  PetscReal :: katt, kdet
  PetscReal :: decayAq, decayIm

  porosity = material_auxvar%porosity
  liquid_saturation = global_auxvar%sat(iphase)
  volume = material_auxvar%volume
  L_water = porosity*liquid_saturation*volume*1.d3  ! 1.d3 converts m^3 water -> L water
  
! Assign concentrations of Vaq and Vim
  Vaq = rt_auxvar%total(this%species_Vaq_id,iphase)
  Vim = rt_auxvar%immobile(this%species_Vim_id)
  PRINT *, "Assigned Vaq/Vim concentrations" ! Edwin debugging    

! initialize all rates to zero
  Rate = 0.d0
  RateAtt = 0.d0
  RateDet = 0.d0

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
  PRINT *, "Assigned attachment/detachment rates" ! Edwin debugging    

  decayAq = this%decay_aqueous
  decayIm = this%decay_adsorbed
  PRINT *, "Assigned decay rates" ! Edwin debugging    

  ! Build here for attachment/detachment
  ! first-order forward - reverse (A <-> C)

  Rate = katt * Vaq * L_water - kdet * Vim * volume
  RateAtt = stoichVaq * Rate
  RateDet = stoichVim * Rate

  ! Build here for inactivation reactions
  ! first-order (A -> C)
  !Rate = decayAq * Vaq * L_water
  !RateA = Rate
  !
  !Rate = decayIm * Vim * volume
  !RateA = Rate

  ! NOTES
  ! 1. Always subtract contribution from residual
  ! 2. Units of residual are moles/second  
  Residual(this%species_Vaq_id) = Residual(this%species_Vaq_id) - RateAtt
  Residual(this%species_Vim_id + reaction%offset_immobile) = &
    Residual(this%species_Vim_id + reaction%offset_immobile) - RateDet
  
end subroutine escPTr_React

subroutine escPTr_Destroy(this)
  ! 
  ! Destroys allocatable or pointer objects created in this
  ! module
  ! 
  ! Author: John Doe
  ! Date: 00/00/00
  ! 

  implicit none
  
  class(reaction_sandbox_escPTr_type) :: this  

! 12. Add code to deallocate contents of the example object

end subroutine escPTr_Destroy

end module Reaction_Sandbox_escPTr_class

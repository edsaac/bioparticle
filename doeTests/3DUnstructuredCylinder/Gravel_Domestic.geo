/*
GMSH .geo file for building a structured mesh of a cilindrical column
*/

// Options for PFLOTRAN export
Mesh.SaveAll = 0;
Mesh.MshFileVersion = 2.2;

// Dimensions of the column
lenghtColumn = 2.00E+01;
diameterColumn = 2.00E+02;
meshSizeZ = 2.50E-01;
meshSizeR = 4.00E+00;

// Conversion factor to SI (m)
convertToMeters = 1./1.;

lenghtColumn *= convertToMeters;
diameterColumn *= convertToMeters;
meshSizeZ *= convertToMeters;
meshSizeR *= convertToMeters;

// Calculate number of elements
nElementsArc = Ceil(Fabs(diameterColumn*Pi/4)/meshSizeR);

If (nElementsArc%2 == 0)
  nElementsArc -= 1;  // Guarantees a node in the middle
EndIf

nElementsRad = Ceil(nElementsArc/2);
nElementsZ = Ceil(Fabs(lenghtColumn)/(meshSizeZ));

// Build points
r = diameterColumn/2;
rsq= r/3.0;
meshSize = 1;

Point(1) = {0,0,0,meshSize};
Point(2) = {r,0,0,meshSize};
Point(3) = {0,r,0,meshSize};
Point(4) = {-r,0,0,meshSize};
Point(5) = {0,-r,0,meshSize};

Point(6) = {rsq,0,0,meshSize};
Point(7) = {0,rsq,0,meshSize};
Point(8) = {-rsq,0,0,meshSize};
Point(9) = {0,-rsq,0,meshSize};


// Build lines
b = 1;
prog = 1.1;
Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2}; 

For i In {1:4}
  Transfinite Line{i} = nElementsArc Using Bump b;
EndFor

Line(5) = {6,7};
Line(6) = {7,8};
Line(7) = {8,9};
Line(8) = {9,6};

For i In {5:8}
  Transfinite Line{i} = nElementsArc Using Bump b;
EndFor

Line(9)  = {6,2}; 
Line(10) = {7,3}; 
Line(11) = {8,4}; 
Line(12) = {9,5};

For i In {9:12}
  Transfinite Line{i} = nElementsRad Using Progression prog;
EndFor

// Build loops
Line Loop(1) = {1,-10,-5,9};
Line Loop(2) = {2,-11,-6,10};
Line Loop(3) = {3,-12,-7,11};
Line Loop(4) = {4,-9,-8,12};
Line Loop(5) = {5,6,7,8};


// Build surfaces
For i In {1:5}
  Plane Surface(i) = {i}; Transfinite Surface {i};
EndFor

Recombine Surface {1 ... 5};

// Build volumes from extrusions
Q1[] = Extrude {0, 0, lenghtColumn} {
    Surface{1};
    Layers{nElementsZ};
    Recombine;
  };

Q2[] = Extrude {0, 0, lenghtColumn} {
    Surface{2};
    Layers{nElementsZ};
    Recombine;
  };
Q3[] = Extrude {0, 0, lenghtColumn} {
    Surface{3};
    Layers{nElementsZ};
    Recombine;
  };
Q4[] = Extrude {0, 0, lenghtColumn} {
    Surface{4};
    Layers{nElementsZ};
    Recombine;
  };
Q5[] = Extrude {0, 0, lenghtColumn} {
    Surface{5};
    Layers{nElementsZ};
    Recombine;
  };

// Assign names [the order these names are assigned = order in msh file]
Physical Volume("wholeDomain") = {Q1[1],Q2[1],Q3[1],Q4[1],Q5[1]};
Physical Surface("bottom") = {1,2,3,4,5};
Physical Surface("top") = {Q1[0],Q2[0],Q3[0],Q4[0],Q5[0]};
Physical Surface("sides") = {Q1[2],Q2[2],Q3[2],Q4[2]};
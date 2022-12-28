Mesh.MshFileVersion = 2.0;

targetSizeFine = 0.15;
targetSizeCoarse = 1.00;

transversalDistance = 5;

Point(1) = {0, 0, 0, targetSizeCoarse};
Point(2) = {transversalDistance, 0, 0, targetSizeFine};
Point(3) = {2.0 * transversalDistance, 0, 0, targetSizeCoarse};

Line(1) = {1,2};
Line(2) = {2,3};


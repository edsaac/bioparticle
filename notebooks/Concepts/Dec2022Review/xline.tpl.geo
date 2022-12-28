Mesh.MshFileVersion = 2.0;

targetSizeFine = 0.10;
targetSizeCoarse = 0.50;

freeBorderDownstream = 10;
setbackDistance = <setbackDistance>;
freeBorderUpstream = 5;

Point(1) = {0, 0, 0, targetSizeCoarse};
Point(2) = {freeBorderDownstream, 0, 0, targetSizeFine};
Point(3) = {freeBorderDownstream + setbackDistance/2, 0, 0, targetSizeCoarse};
Point(4) = {freeBorderDownstream + setbackDistance, 0, 0, targetSizeFine};
Point(5) = {freeBorderDownstream + setbackDistance + freeBorderUpstream, 0, 0, targetSizeCoarse};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};


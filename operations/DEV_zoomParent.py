"""

SHAPE NODE CONSOLIDATOR
WITH ZOOM CORRECTION

Function to move all shape nodes from objects
selected under the Transform of LAST selected object.

"""


def makeZoomCurve(selectionList):
    # Store selected objs
    selection = selectionList

    # Final Coord vars
    bboxNeg = [0.000, 0.000, 0.000]
    bboxPos = [0.000, 0.000, 0.000]

    # Initial N
    n = 0

    # Nested Lists def
    bboxList = [[], [], [], [], [], []]

    # Initial loop to correct transforms and find bounding box for zoom correction
    for obj in selection:

        # Freeze transforms to prevent movement on run
        cd.makeIdentity(obj, a=1, t=1, r=1, s=1)

        # Bounding box,
        bbox = cd.xform(obj, q=True, boundingBox=True)

        # Loop through bbox values
        for i in range(len(bbox)):
            # Append to nested lists for min/max later
            bboxList[i].append(bbox[i])

        # Print Test
        #    print(len(bbox))
        #    print(len(bboxList))
        print(bboxList)

        # Shape's bbox coords
        bboxNeg = [min(bboxList[0]), min(bboxList[1]), min(bboxList[2])]
        bboxPos = [max(bboxList[3]), max(bboxList[4]), max(bboxList[5])]

    # test positions
    # cd.spaceLocator(name="{}_{}".format(obj, "negBox01"), p=bboxNeg)
    # cd.spaceLocator(name="{}_{}".format(obj, "posBox01"), p=bboxPos)

    zoomCurve = cd.curve(
        n=selection[-1],
        d=1,
        p=[
            bboxNeg,
            bboxPos,
        ]
    )


def Object_Consolidator(*args):

    selection = cd.ls(sl=True, fl=True)

    # Initial loop to correct transforms and find bounding box for zoom correction
    for obj in selection:
        # Freeze transforms to prevent movement on run
        cd.makeIdentity(obj, a=1, t=1, r=1, s=1)




    # Stores final curve as parent
    parentTransform = selection[-1]

    # Stores objs to parent
    objsToParent = selection[0:-1]

    # Loop through each object
    for obj in objsToParent:

        # Shape nodes of each object
        shapeNodes = cd.listRelatives(o, s=True)

        # Loop through all shapes
        for shape in shapeNodes:
            # Parents the shape node under the parent's transform
            cd.parent(shape, parentTransform, s=True, r=True)

            # Delete the old empty transform
            cd.delete(obj)

            # Centre pivot on new transform
            cd.xform(cp=True)

            # Finally selects the object
            cd.select(parentTransform)

    # Then correct zoom bounds.
    cd.exact

# Run function
shapeNodeConsolidator()
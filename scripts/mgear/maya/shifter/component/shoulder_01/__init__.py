"""Component Shoulder 01 module"""

from pymel.core import datatypes

from mgear.maya.shifter import component

from mgear.maya import transform, primitive, vector

#############################################
# COMPONENT
#############################################


class Component(component.Main):
    """Shifter component Class"""

    # =====================================================
    # OBJECTS
    # =====================================================
    def addObjects(self):
        """Add all the objects needed to create the component."""

        self.normal = self.guide.blades["blade"].z * -1
        self.binormal = self.guide.blades["blade"].x

        self.length0 = vector.getDistance(self.guide.apos[0],
                                          self.guide.apos[1])

        t = transform.getTransformLookingAt(self.guide.apos[0],
                                            self.guide.apos[1],
                                            self.normal,
                                            axis="xy",
                                            negate=self.negate)

        self.ctl_npo = primitive.addTransform(
            self.root, self.getName("ctl_npo"), t)

        self.ctl = self.addCtl(
            self.ctl_npo,
            "ctl",
            t,
            self.color_fk,
            "cube",
            w=self.length0,
            h=self.size * .1,
            d=self.size * .1,
            po=datatypes.Vector(.5 * self.length0 * self.n_factor, 0, 0),
            tp=self.parentCtlTag)

        t = transform.getTransformFromPos(self.guide.apos[1])
        self.orbit_ref1 = primitive.addTransform(
            self.ctl, self.getName("orbit_ref1"), t)
        self.orbit_ref2 = primitive.addTransform(
            self.root, self.getName("orbit_ref2"), t)
        self.orbit_cns = primitive.addTransform(
            self.ctl, self.getName("orbit_cns"), t)

        self.orbit_npo = primitive.addTransform(
            self.orbit_cns, self.getName("orbit_npo"), t)

        self.orbit_ctl = self.addCtl(self.orbit_npo,
                                     "orbit_ctl",
                                     t,
                                     self.color_fk,
                                     "sphere",
                                     w=self.length0 / 4,
                                     tp=self.ctl)

        self.jnt_pos.append([self.ctl, "shoulder"])

    # =====================================================
    # ATTRIBUTES
    # =====================================================
    def addAttributes(self):
        """Create the anim and setupr rig attributes for the component"""

        # Ref
        if self.settings["refArray"]:
            ref_names = self.settings["refArray"].split(",")
            if len(ref_names) >= 1:
                self.ref_att = self.addAnimEnumParam(
                    "rotRef", "Ref", 0, self.settings["refArray"].split(","))

    # =====================================================
    # OPERATORS
    # =====================================================
    def addOperators(self):
        """Create operators and set the relations for the component rig

        Apply operators, constraints, expressions to the hierarchy.
        In order to keep the code clean and easier to debug,
        we shouldn't create any new object in this method.

        """
        return

    # =====================================================
    # CONNECTOR
    # =====================================================
    def setRelation(self):
        """Set the relation beetween object from guide to rig"""
        self.relatives["root"] = self.ctl
        self.relatives["tip"] = self.orbit_ctl

        self.controlRelatives["root"] = self.ctl
        self.controlRelatives["tip"] = self.orbit_ctl

        self.jointRelatives["root"] = 0
        self.jointRelatives["tip"] = 0

    def connect_standard(self):
        self.parent.addChild(self.root)
        self.connect_standardWithRotRef(self.settings["refArray"],
                                        self.orbit_cns)

# -*- coding: utf-8 -*-
'''
Functions that are in development.
'''
import pickle, gapageconfig

def LoadMUSets():
    '''
    () -> dictionary

    For use in model building workflow.  Returns a dictionary with map unit sets
    and their descriptions, along with an entry that lists all of the map unit
    sets included in the dictionary.
    '''
    filename = open(gapageconfig.wildclass, "rb")
    MUSets = pickle.load(filename)
    filename.close()
    return MUSets

###############  Working lists of map unit types for filtering & model building.  These should be eventually
# removed from this module and put in Make Wildlife Habita Classification Dictionary pkl.py.
def MULists():
    '''
    () -> tuple

    Returns a list of the names of various MU lists that Nate has made.
    '''
    return ('MUAquatic', 'MUPlaya', 'MUDeveloped', 'MUMudflat', 'MUOrchards', 'MURowCrops', 'MUNeedleTree',
            'MUBroadTree', 'MUSagebrush', 'MUForest', 'MUWoodland', 'MUhasSaturatedSoil', 'MUisSaturatedSoil')


def MUisSaturatedSoil():
    '''
    () -> tuple

    Returns a tuple of systems that are always (rare droughts aside) wet or
    saturated with water throughout.  Seasonally flooded systems are not
    included here.
    '''
    isSat = (9101, 9243, 9103, 9230, 9105, 4553, 9104, 9215, 9301, 9233, 9109,
            9235, 9218, 9401, 9501, 9222, 9212, 5701, 4550, 9210, 9605, 9232,
            9110, 5607, 9229, 9213, 9220, 9403, 9308, 9242, 9224, 9214, 9505,
            9504, 9106, 9227, 9502, 9306, 9226, 9216, 9234, 9304, 9606, 9503,
            8504, 9238, 9702, 9718, 9236, 9239, 9204, 9201, 9703, 5606, 9506,
            9225, 9228, 3402, 3401, 9108, 9853, 9237, 9607)
    return isSat


def MUhasSaturatedSoil():
    '''
    () -> tuple

    Returns a tuple of systems with soils that are constantly or very frequently
    saturated.  Must have soils capable of holding water for the length of time
    between flood events for at least one season.  This is meant to be useful
    for species that need wet, saturated soils found in places like swamps and
    marshes.  Includes tidal marshes and swamps, but not sandy beaches because
    the sands drain between floods or heavy rains. Rocky or cobble substrate not
    considered a “soil” for this set.  Systems with soils that are flooded for
    an entire season are included.  Mesic forests that could contain small seeps
    are not included, the systems included have larger wetlands within them as
    specified by the description.  Consider creating a companion list of systems
    that could contain small seeps and fens. Wet meadows are included.
    '''
    hasSat = (9101, 5105, 9801, 9845, 9243, 4210, 9103, 9303, 9206, 9716, 9230,
             9105, 4504, 4553, 4505, 4506, 9104, 9215, 9301, 9302, 9233, 4211,
             9109, 9235, 9207, 9843, 9842, 7503, 4212, 9218, 9907, 9211, 9401,
             9501, 9809, 9802, 9906, 9712, 9231, 9909, 9818, 9222, 9212, 7508,
             9610, 5701, 9831, 9609, 9708, 1402, 1204, 1202, 1203, 1201, 8103,
             8102, 4550, 7506, 9804, 9807, 4150, 9910, 9902, 9903, 9904, 9603,
             9851, 9713, 9911, 9210, 4142, 4141, 9815, 9817, 4131, 9605, 9232,
             9110, 9223, 5607, 9221, 9229, 7402, 9402, 9705, 9213, 9220, 8108,
             8106, 8107, 9714, 9403, 9855, 8406, 4517, 9308, 9820, 9242, 9224,
             9214, 7602, 9701, 4151, 9915, 9849, 9505, 9846, 9504, 9717, 9854,
             9836, 9827, 9106, 5509, 9227, 9502, 9306, 4613, 9226, 9811, 9812,
             9216, 9914, 9240, 7507, 9601, 9709, 9234, 9304, 9824, 9704, 4138,
             9826, 9847, 1401, 1403, 1301, 8304, 8101, 9844, 5103, 9606, 9825,
             9813, 9503, 7205, 9837, 8504, 9238, 9702, 9305, 9219, 9718, 9236,
             9905, 9602, 7510, 4206, 9912, 9857, 9805, 9808, 9850, 9852, 9241,
             9239, 9202, 9205, 9204, 9203, 9201, 9703, 9208, 9806, 9715, 5606,
             9506, 8105, 9225, 9228, 3402, 3401, 9608, 9108, 9604, 7505, 9853,
             8104, 9840, 9237, 5514, 9916, 9913, 9209, 9839, 7320, 9908, 9710,
             9706, 9823, 9814, 9707, 9848, 9711, 9607)
    return hasSat


def MUisAquatic():
    '''
    () -> tuple

    Returns a tuple of water and eelgrass bed MU's.
    '''
    Aquatic = (9107, 9102, 2104, 2103, 2102)
    return Aquatic

def MUisPlaya():
    '''
    () -> tuple

    Returns a tuple of playa MU's.
    '''
    Playa = (3407, 3405)
    return Playa

def MUisDeveloped():
    '''
    () -> tuple

    Returns a tuple of developed MU's.
    '''
    Developed = (1204, 1202, 1203)
    return Developed

def MUisMudflat():
    '''
    () -> tuple

    Returns a tuple of mudflat MU's.
    '''
    Mudflat = (3402, 3401)
    return Mudflat

def MUisOrchard():
    '''
    () -> tuple

    Returns a tuple of orchard and 'high structure agriculture' MU's.
    '''
    Orchards = (1401)
    return Orchards

def MUisRowCrop():
    '''
    () -> tuple

    Returns a tuple of row crop MU's.
    '''
    RowCrops = (1402)
    return RowCrops


def MUhasNeedleTree():
    '''
    () -> tuple

    Returns a tuple of MU's that potentially have some coniferous tree component,
    which could be very little.  Could be forest or woodland. Includes Taxodium (cypress)
    but not Juniper.
    '''
    NeedleTree = (4333, 4551, 5107, 4126, 4307, 4331, 4314, 9801, 9845, 9303, 9716, 4504, 4553,
    4505, 4506, 4403, 9301, 9302, 4211, 9235, 9207, 9843, 9842, 4212, 9218, 9907, 9211, 4536, 5602, 4201,
    4535, 4326, 4545, 4601, 5503, 4520, 5403, 5404, 5511, 4330, 4335, 9906, 3213, 9909, 3205, 5512, 4325,
    9212, 4101, 4612, 4511, 3218, 5601, 4512, 9831, 4513, 1202, 1203, 4602, 4550, 4303, 4301, 4309, 4507,
    4501, 4508, 4509, 9901, 7321, 9804, 4102, 4150, 9910, 9902, 9903, 9904, 4306, 4128, 4103, 4105, 4205,
    9603, 9911, 4209, 9210, 4541, 9829, 8202, 4502, 4503, 5214, 9830, 4514, 9213, 8106, 4324, 3216, 5603,
    9855, 4515, 3214, 4516, 4517, 5516, 4542, 5515, 9308, 4113, 4323, 4327, 9214, 9701, 4143, 4315, 4518,
    4316, 8203, 4519, 9849, 4317, 4603, 4404, 4320, 4318, 4521, 4543, 4153, 9717, 9854, 9836, 9827, 9502,
    4319, 4547, 9306, 7604, 4604, 4613, 4338, 3124, 4522, 4605, 4606, 4607, 7202, 3209, 9812, 4523, 4110,
    3404, 4552, 3208, 7312, 4106, 4304, 4104, 4114, 4539, 9240, 7507, 4540, 9601, 4608, 4337, 9307, 9304,
    4524, 5302, 9824, 4609, 4529, 4525, 4510, 9704, 4548, 4549, 4328, 5517, 9844, 3202, 4526, 4527, 9825,
    5806, 4544, 4531, 4611, 4532, 9832, 3215, 4533, 4546, 9238, 9702, 9305, 9905, 4145, 4402, 4322, 4538,
    4537, 9852, 9239, 9203, 9201, 9703, 4146, 4329, 4305, 4310, 4311, 5508, 9806, 4202, 4334, 4308, 4528,
    4610, 7206, 4534, 5605, 4530, 9506, 4401, 5513, 9840, 4204, 9237, 9916, 9913, 4332, 4336, 4321, 9908,
    5505, 9402)
    return NeedleTree

def MUhasBroadTree():
    '''
    () -> tuple

    Returns a tuple of MU's with potentially some broad-leaved tree component, which could be very little.
    Could be forest or woodland.  Does not include Mountain Curl-leaf Mahogany as a tree.
    '''
    BroadTree = (4333, 4126, 4307, 4331, 4314, 7313, 9801, 9845, 4210, 9303, 9716, 4133, 4504, 4553,
    4505, 4506, 9215, 4403, 9301, 9302, 4211, 9235, 9843, 9842, 4212, 9218, 9211, 5602, 9501, 4201, 4535,
    4326, 5501, 9809, 5502, 5503, 5403, 5404, 5511, 9802, 4330, 4335, 9803, 5512, 4325, 9818, 9819, 9212,
    7302, 4136, 4127, 4101, 4511, 9831, 4513, 4118, 9828, 8201, 1202, 1203, 4550, 4303, 4301, 4309, 4507,
    4501, 4509, 9901, 7321, 9804, 4102, 4150, 9902, 9904, 4117, 4306, 4128, 4103, 4105, 4205, 9851, 9911,
    4129, 4209, 9210, 4142, 4140, 4141, 9815, 9817, 4131, 7301, 4155, 4152, 5811, 4208, 9829, 8202, 5214,
    9830, 9213, 4324, 9855, 8401, 4516, 4517, 5515, 9308, 9820, 4113, 4323, 4327, 9214, 7602, 9701, 4151,
    9915, 4143, 4315, 4316, 8203, 9849, 4317, 4404, 4320, 4144, 4139, 9717, 9854, 9836, 9827, 5509, 9833,
    9856, 9835, 4148, 4319, 9306, 7604, 4338, 9811, 9812, 4110, 3207, 4123, 4121, 4120, 4124, 5506, 7312,
    9914, 5507, 4106, 4304, 4104, 4114, 4539, 9240, 4313, 4540, 4337, 9824, 9704, 4138, 9826, 9847, 1401,
    4122, 4149, 4115, 4207, 9858, 4549, 4328, 5517, 9844, 4107, 4111, 4112, 9825, 9813, 9832, 9238, 4132,
    9912, 9857, 9805, 4402, 9850, 4206, 4135, 4119, 5504, 9852, 4130, 9838, 9239, 9202, 9703, 4146, 9208,
    4203, 4116, 4329, 4302, 4310, 4311, 5508, 9806, 4202, 9841, 9715, 4334, 4610, 7206, 9506, 4401, 4125,
    4109, 4134, 9816, 7322, 5513, 4137, 9840, 4204, 9237, 5514, 9916, 9913, 4332, 4336, 9209, 9839, 4312,
    9823, 9814, 4154, 5505, 9846, 7319, 9402)
    return BroadTree

def MUhasShrubDom():
    '''
    () -> tuple

    Returns a tuple of MU's that include any amount of shrub dominated areas.
    Steppe is included but other systems with only intermittent shrub cover are
    not (such as badlands or cliffs).  Woodlands and savannahs with shrub understory
    but sparse tree cover are not included.  Cultivated Cropland is not included.
    '''
    Shrub = (9216, 9222, 5217, 9224, 5207, 9231, 9234, 5209, 9242, 9243, 5210, 5211,
    5201, 4136, 5212, 3116, 9821, 3121, 4147, 4148, 5214, 4154, 5301, 5216, 5701, 5702,
    5703, 5704, 5705, 5706, 5707, 9807, 9808, 9809, 5202, 5203, 5204, 5205, 5206, 9815,
    5208, 9817, 9818, 9819, 9820, 5213, 9822, 5215, 9824, 9825, 5218, 9828, 9830, 9831,
    9833, 9834, 9835, 9837, 8304, 4210, 4211, 4212, 9847, 9848, 9850, 9856, 9857, 7303,
    3217, 3218, 7318, 5801, 5803, 5804, 5805, 5806, 5405, 5808, 5809, 5810, 5811, 5812,
    5406, 5303, 5304, 5305, 5306, 5307, 5308, 5309, 5408, 9506, 8402, 8406, 3602, 9811,
    5401, 5402, 5403, 5404, 9501, 9502, 5407, 9504, 5409, 5410, 5411, 4404, 8504, 5807,
    7509, 5507, 9604, 9609, 5516, 5104, 8102, 5105, 8104, 8105, 8107, 7601, 7603, 5108,
    5601, 5602, 5607, 9708, 9810, 5102, 5103, 9712, 9713, 5106, 5107, 9716, 9205, 9207,
    9812, 9846)
    return Shrub


def MUhasOpen():
    '''
    () -> tuple

    Returns a tuple of MU's with the possibility of sizable areas without trees.
    Includes marsh, some glades (revise?), rock outcrops, steppe, and others but does
    not include woodlands, flatwoods, savannahs, or shrub-dominated
    areas (could be added via union with MUShrubDom).
    '''
    Open2 = (9219, 9220, 9221, 9222, 9223, 9224, 9225, 9226, 9303, 4108, 9229, 9230,
    9231, 9232, 3601, 9234, 3603, 3604, 3605, 3606, 3607, 9241, 9242, 9243, 3105,
    3106, 3107, 7204, 7205, 7206, 3111, 3112, 3113, 3114, 3115, 3116, 3117, 3118,
    3119, 3120, 3121, 3122, 3123, 3124, 3125, 2102, 2103, 2104, 9227, 5702, 5704,
    9228, 9807, 9808, 9810, 9814, 9815, 9817, 9818, 9819, 9820, 9822, 9823, 9826,
    9403, 9828, 9829, 9233, 9831, 8301, 7505, 8303, 9847, 9850, 9853, 3201, 3202,
    3203, 3204, 7301, 3206, 7303, 7304, 7305, 7306, 7307, 3212, 3213, 3214, 3215,
    3216, 7313, 3218, 7315, 3220, 7317, 7318, 7320, 7321, 7322, 7323, 7324, 7326,
    7308, 9606, 5802, 5807, 1201, 5303, 5304, 9401, 5306, 5307, 5308, 5309, 5513,
    7201, 7202, 9503, 4131, 8404, 8405, 8406, 8407, 8408, 3108, 4314, 3110, 3602,
    3109, 5105, 4325, 3302, 3303, 3304, 7401, 3306, 8403, 9709, 7203, 9608, 9607,
    9857, 1301, 5505, 9710, 9502, 5509, 9504, 9505, 9506, 7302, 3207, 3208, 8501,
    8502, 3209, 5517, 3210, 3211, 3401, 3402, 3403, 7501, 7502, 7503, 7504, 8504,
    7506, 7507, 7508, 7310, 7510, 7311, 3301, 7312, 3217, 7314, 7309, 3219, 3305,
    7316, 1403, 7402, 3221, 9601, 9602, 9603, 9604, 9605, 5510, 5511, 5512, 9609,
    9610, 5515, 5516, 9101, 9102, 9103, 9104, 9105, 9106, 9107, 9108, 9109, 9110,
    8101, 8103, 8104, 8108, 3501, 3502, 3503, 3504, 7601, 3506, 7603, 7604, 9204,
    7101, 7102, 7103, 7104, 5305, 9718, 8503, 5514, 3405, 4107, 3406, 3407, 5607,
    9705, 9706, 9707, 9708, 5101, 5102, 9711, 9712, 9713, 9714, 5107, 9716, 9206,
    9215, 9846, 9402, 1402)
    return Open2

def MUhasSagebrush():
    '''
    () -> tuple

    Returns a tuple of sagebrush MU's.
    '''
    Sagebrush = (3111, 3121, 3216, 3304, 3403, 3407, 4147, 4512, 4513, 4514, 4520,
                 4526, 4529, 4530, 4534, 4550, 5104, 5203, 5210, 5301, 5302, 5305,
                 5306, 5307, 5308, 5309, 5601, 5701, 5702, 5703, 5704, 5705, 5706,
                 5707, 5803, 5809, 7303, 7305, 9609, 9708, 9810, 9830, 9848)
    return Sagebrush

def MUhasForest():
    '''
    () -> tuple

    Returns a tuple of MU's that have some forest component, which could be very little.
    MU's were included if the description or name of the MU explicititly stated "forest"
    or if I interpreted it to include dense canopy cover. Swamps included in this list.
    '''
    Forest = (4333, 4551, 4126, 4307, 4331, 9801, 9845, 4210, 4133, 4504, 4553, 4505, 4506, 9215,
    4403, 9301, 9302, 4211, 9235, 9843, 9842, 4212, 9218, 9211, 9501, 4201, 4535, 4326, 4545, 5502,
    4601, 5511, 9802, 4330, 9803, 9818, 9819, 9212, 4136, 4127, 4101, 4612, 9831, 4118, 8201, 4602,
    4550, 4301, 4309, 4507, 4501, 4509, 9804, 4102, 4150, 9910, 9902, 9904, 4117, 4306, 4128, 4103,
    4105, 4205, 9851, 9911, 4129, 4209, 9210, 4142, 4541, 4140, 4141, 9815, 9817, 4155, 4152, 4208,
    8202, 9830, 9402, 9213, 8106, 4324, 9855, 8401, 4542, 9308, 9820, 4113, 4323, 4327, 9214, 7602,
    9701, 4151, 4315, 4316, 8203, 4519, 9849, 4317, 4603, 4320, 4318, 4543, 4153, 4139, 9717, 9854,
    9836, 9827, 9833, 9856, 9502, 4148, 4319, 4547, 9306, 7604, 4604, 4613, 4338, 9811, 3124, 4522,
    4605, 4606, 4607, 9812, 4523, 4110, 3404, 4552, 3207, 4123, 4121, 4120, 4124, 9914, 4106, 4304,
    4104, 4114, 4539, 9240, 4313, 9601, 4337, 9304, 4524, 9824, 4609, 9704, 4548, 4138, 9826, 1401,
    4122, 4149, 4115, 4207, 9858, 4328, 9844, 4111, 4527, 9813, 4544, 4531, 4611, 9832, 4533, 9238,
    9702, 4132, 9857, 9805, 4402, 9850, 4135, 4322, 4538, 4537, 4119, 9852, 4130, 9838, 9239, 9202,
    9203, 9201, 9703, 4146, 9208, 4203, 4116, 4329, 4302, 4305, 4310, 4311, 9806, 4202, 9841, 9715,
    4334, 4308, 4528, 4610, 9506, 4401, 4125, 4109, 4134, 4137, 9840, 4204, 9237, 9916, 9913, 4332,
    4336, 9209, 9839, 4321, 4312, 9823, 9814, 4154)
    return Forest

def MUhasWoodland():
    '''
    () -> tuple

    Returns a tuple of MU's that have some woodland, savanna, flatwoods, or very open tree
    canopy.  MU's were included if the description or name of the MU explicititly stated
    "woodland", "savanna", or "flatwoods" or if I interpreted it to include open canopy.
    The list doesn't include systems that have at most a sparse occurrence of trees.
    Pinyon-juniper woodlands included but not if they were stunted and shrubland like.
    I considered Curl-leaf Mountain Mahogany a shrub, so woodland of it was not inluded
    in this list.  I did include dwarf cypress savanna.
    '''
    Woodland = (5107, 4126, 4307, 4314, 7313, 9303, 9716, 4504, 4553, 4505, 4506, 9207, 9907, 4536,
    5501, 9809, 4545, 5502, 5503, 4520, 5403, 5511, 4330, 4335, 9906, 9909, 3205, 5512, 4325, 9819,
    7302, 4136, 4511, 3218, 4512, 9831, 4513, 4118, 9828, 1202, 1203, 4602, 4550, 4303, 4301, 4309,
    4508, 4509, 9901, 7321, 4102, 9910, 9903, 9603, 9911, 4541, 4140, 4131, 7301, 4155, 4152, 9829,
    4502, 4503, 9830, 4514, 5607, 9402, 4324, 5603, 9855, 4515, 4516, 4517, 5516, 5515, 7602, 4151,
    9915, 4143, 5604, 4315, 4518, 4316, 4519, 9849, 4317, 4603, 4404, 4144, 4318, 9846, 4521, 4543,
    5509, 9833, 9835, 4319, 4338, 9811, 4605, 9812, 4523, 4110, 3404, 4552, 3207, 4121, 4120, 5506,
    9914, 5507, 4106, 4304, 4104, 4539, 7507, 4540, 9601, 4608, 9307, 4524, 5302, 9824, 4529, 4525,
    4510, 4548, 4138, 9847, 1401, 4122, 4149, 4115, 4549, 4328, 5517, 4107, 4111, 4112, 4526, 4527,
    9825, 9813, 4531, 4611, 4532, 9832, 4533, 4546, 9305, 9905, 4145, 4206, 9912, 9850, 4322, 4537,
    5504, 4305, 5508, 4202, 4528, 5606, 4610, 4534, 5605, 4530, 9816, 7322, 5513, 4137, 9916, 9913,
    4332, 4336, 4321, 9908, 4312, 4154, 5505)
    return Woodland

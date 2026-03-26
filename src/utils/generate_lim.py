from hashlib import sha256
from src.utils.Random import Random
from src.utils.lims.type_one.one_one import generate_lim_1_1
from src.utils.lims.type_one.one_two import generate_lim_1_2
from src.utils.lims.type_one.one_three import generate_lim_1_3
from src.utils.lims.type_one.one_four import generate_lim_1_4
from src.utils.lims.type_one.one_five import generate_lim_1_5
from src.utils.lims.type_two.two_one import generate_lim_2_1
from src.utils.lims.type_two.two_two import generate_lim_2_2
from src.utils.lims.type_two.two_three import generate_lim_2_3
from src.utils.lims.type_two.two_four import generate_lim_2_4
from src.utils.lims.type_two.two_five import generate_lim_2_5
from src.utils.lims.type_three.three_one import generate_lim_3_1
from src.utils.lims.type_three.three_two import generate_lim_3_2
from src.utils.lims.type_three.three_three import generate_lim_3_3
from src.utils.lims.type_three.three_four import generate_lim_3_4
from src.utils.lims.type_three.three_five import generate_lim_3_5
from src.utils.lims.type_three.three_six import generate_lim_3_6
from src.utils.lims.type_four.four_one import generate_lim_4_1
from src.utils.lims.type_four.four_two import generate_lim_4_2
from src.utils.lims.type_four.four_three import generate_lim_4_3
from src.utils.lims.type_four.four_four import generate_lim_4_4
from src.utils.lims.type_four.four_five import generate_lim_4_5
from src.utils.lims.type_five.five_one import generate_lim_5_1
from src.utils.lims.type_six.six_one import generate_lim_6_1
from src.utils.lims.type_six.six_two import generate_lim_6_2
from src.utils.lims.type_six.six_three import generate_lim_6_3
from src.utils.lims.type_seven.seven_one import generate_lim_7_1
from src.utils.lims.type_seven.seven_two import generate_lim_7_2
import os

async def generate_lims(counts, seed):
    rand = Random(seed)
    primers = []
    type_one = [generate_lim_1_2] # generate_lim_1_2, generate_lim_1_3, generate_lim_1_4, generate_lim_1_5]
    type_two = [generate_lim_2_1, generate_lim_2_2, generate_lim_2_3, generate_lim_2_4, generate_lim_2_5]
    type_three = [generate_lim_3_1, generate_lim_3_2, generate_lim_3_3, generate_lim_3_4, generate_lim_3_5, generate_lim_3_6]
    type_four = [generate_lim_4_1, generate_lim_4_2, generate_lim_4_3, generate_lim_4_4, generate_lim_4_5]
    type_five = [generate_lim_5_1]
    type_six = [generate_lim_6_1, generate_lim_6_2, generate_lim_6_3]
    type_seven = [generate_lim_7_1, generate_lim_7_2]

    for _ in range(counts[0]):
        primers += await rand.choice(type_one)(rand, 1)
    for _ in range(counts[1]):
        primers += await rand.choice(type_two)(rand, 1)
    for _ in range(counts[2]):
        primers += await rand.choice(type_three)(rand, 1)
    for _ in range(counts[3]):
        primers += await rand.choice(type_four)(rand, 1)
    for _ in range(counts[4]):
        primers += await rand.choice(type_five)(rand, 1)
    for _ in range(counts[5]):
        primers += await rand.choice(type_six)(rand, 1)
    for _ in range(counts[6]):
        primers += await rand.choice(type_seven)(rand, 1)

    return primers
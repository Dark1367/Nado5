from hashlib import sha256
from src.utils.Random import Random
from src.utils.lims.type_one.one_one import gen_one_one_lim
from src.utils.lims.type_one.one_two import gen_one_two_lim
from src.utils.lims.type_one.one_three import gen_one_three_lim
from src.utils.lims.type_one.one_four import gen_one_four_lim
from src.utils.lims.type_one.one_five import gen_one_five_lim
from src.utils.lims.type_two.two_one import gen_two_one_lim
from src.utils.lims.type_two.two_two import gen_two_two_lim
from src.utils.lims.type_two.two_three import gen_two_three_lim
from src.utils.lims.type_two.two_four import gen_two_four_lim
from src.utils.lims.type_two.two_five import gen_two_five_lim
from src.utils.lims.type_three.three_one import gen_three_one_lim
from src.utils.lims.type_three.three_two import gen_three_two_lim
from src.utils.lims.type_three.three_three import gen_three_three_lim
from src.utils.lims.type_three.three_four import gen_three_four_lim
from src.utils.lims.type_three.three_five import gen_three_five_lim
from src.utils.lims.type_three.three_six import gen_three_six_lim
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

rand = Random(str(os.urandom(8)))

async def generate_lims(counts):
    primers = []
    type_one = [gen_one_one_lim, gen_one_two_lim, gen_one_three_lim, gen_one_four_lim, gen_one_five_lim]
    type_two = [gen_two_one_lim, gen_two_two_lim, gen_two_three_lim, gen_two_four_lim, gen_two_five_lim]
    type_three = [gen_three_one_lim, gen_three_two_lim, gen_three_three_lim, gen_three_four_lim, gen_three_five_lim, gen_three_six_lim]
    type_four = [generate_lim_4_1, generate_lim_4_2, generate_lim_4_3, generate_lim_4_4, generate_lim_4_5]
    type_five = generate_lim_5_1
    type_six = [generate_lim_6_1, generate_lim_6_2, generate_lim_6_3]
    type_seven = [generate_lim_7_1, generate_lim_7_2]

    primers += await rand.choice(type_one)(counts[0])
    primers += await rand.choice(type_two)(counts[1])
    primers += await rand.choice(type_three)(counts[2])
    primers += await rand.choice(type_four)(counts[3])
    primers += await type_five(counts[4])
    primers += await rand.choice(type_six)(counts[5])
    primers += await rand.choice(type_seven)(counts[6])

    return primers
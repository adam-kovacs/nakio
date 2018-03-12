
#List of Obstacle Class Parameters
#[file source, starting y position, if animated, speed, jump velocity]

car1 = ["images/car1", 295, True, 4, 0]
car2 = ["images/car2", 280, True, 3, 0]
car3 = ["images/car3", 307, True, 3.5, 0]
car4 = ["images/car4", 307, True, 3.5, 0]
car5 = ["images/car5", 290, True, 3.5, 0]
car6 = ["images/car6", 285, True, 3, 0]
car7 = ["images/car7", 285, True, 3, 0]
car8 = ["images/car8", 304, True, 5, 0]
car9 = ["images/car9", 304, True, 4.5, 0]

slo1 = ["images/slo1", 304, True, 2.5, 0]
slo2 = ["images/slo2", 307, True, 2.5, 3.5]
slo3 = ["images/slo3", 270, True, 3.5, 2]
slo4 = ["images/slo4", 250, True, 2, 0]
slo5 = ["images/slo5", 307, True, 2.1, 0]
slo6 = ["images/slo6", 303, True, 2.2, 0]
slo7 = ["images/slo7", 307, True, 3, 0]
slo8 = ["images/slo8", 307, True, 2, 0]
slo9 = ["images/slo9", 307, True, 1.8, 0]
slo10 = ["images/slo10", 307, True, 2, 0]

obs1 = ["images/obs1", 315, False, 1.5, 0]
obs2 = ["images/obs2", 325, False, 1.5, 0]
obs3 = ["images/obs3", 293, False, 1.5, 0]
obs4 = ["images/obs4", 293, False, 1.5, 0]
obs5 = ["images/obs5", 293, False, 1.5, 0]
obs6 = ["images/obs6", 265, False, 1.5, 0]
obs7 = ["images/obs7", 286, False, 1.5, 0]

street1 = ["images/streetloop_1", 329, False, 1.5, 0]
street2 = ["images/streetloop_2", 329, False, 1.5, 0]
street3 = ["images/streetloop_3", 329, False, 1.5, 0]
street4 = ["images/streetloop_4", 329, False, 1.5, 0]



#Lists of Obstacles, depending on current Level
carlist_1 = [car1, car3, car4, car5, car7]
slolist_1 = [slo3, slo5, slo6, slo7, slo10]
carlist_2 = [car3, car4, car5, car6, car7, car9]
slolist_2 = [slo1, slo3, slo4, slo5, slo6, slo7, slo9]
carlist_3 = [car2, car6, car8, car9]
slolist_3 = [slo1, slo2, slo3, slo4, slo6, slo7, slo8]


#-------------------------------------------------------------------------------


#Lists of Obstacle parameters and lists which are directly imported to nakio.py
streetlist = [street1, street2, street3, street4]
obslist = [obs1, obs2, obs3, obs4, obs5, obs6, obs7]
movelist= [carlist_1, slolist_1, carlist_2, slolist_2, carlist_3, slolist_3]



constants = {'fusion': 334.4, 'vaporization': 2259, 'heatice': 2.09, 'heatwater': 4.184, 'heatsteam': 1.84}
kj_constants = {'fusion': 6.02, 'vaporization': 40.6, 'heatice': 0.0371, 'heatwater': 0.0753, 'heatsteam': 0.0331}


def thermo(mass, temp, temp2, const):
    # Change S to constants or kj depending on kj or joules
    if const:
        s = constants
    else:
        s = kj_constants

    if temp < 0:
        fusion = abs(temp)
        energy1 = s['heatice'] * mass * fusion
        phasechange = s['fusion'] * mass

        if temp2 >= 100:
            energy2 = s['heatwater'] * mass * 100
            phasechange2 = s['vaporization'] * mass
            heat2 = abs(temp2 - 100)
            energy4 = s['heatsteam'] * mass * heat2
            return phasechange + energy1 + energy2 + energy4 + phasechange2

        else:
            heat = abs(temp2)
            energy3 = heat * s['heatwater'] * mass
            return energy1 + phasechange + energy3

    else:
        if temp2 >= 100:
            t1 = 100 - temp
            eng1 = s['heatwater'] * t1 * mass
            pchange = s['vaporization'] * mass
            t2 = temp2 - 100
            eng2 = s['heatsteam'] * mass * t2
            return eng1 + pchange + eng2

        else:
            t3 = temp2 - temp
            energy = t3 * mass * s['heatwater']
            return energy
import pandas as pd
import math
import scipy.optimize as opt


def calcRatingDiff(df):
    df['rating_diff'] = None
    for index, row in df.iterrows():
        pHome = 1 / row['home_odds']
        pDraw = 1 / row['draw_odds']
        pAway = 1 / row['away_odds']
        ratingDiff0 = 70  # home field advatage
        result = opt.minimize(calcLeastSquare, ratingDiff0, args=(pHome, pDraw, pAway), method='powell')
        df.loc[index, 'rating_diff'] = result.x[0]
    return df


def calcLeastSquare(ratingDiff, *pOdds):
    pHomeOdds, pDrawOdds, pAwayOdds = pOdds

    ExGpmHome, ExGpmAway = calcExGpm(ratingDiff)
    pHomeModel, pDrawModel, pAwayModel = calcP(ExGpmHome, ExGpmAway)

    leastSquare = ((pHomeModel - pHomeOdds) ** 2
                   + (pDrawModel - pDrawOdds) ** 2
                   + (pAwayModel - pAwayOdds) ** 2)
    return leastSquare


def calcExGpm(ratingDiff):
    minutes = 90
    paramA = 650  # default: 650
    paramB = 200  # default: 200
    ExGpmHome = math.exp(1 / paramA * (ratingDiff + paramB)) / minutes
    ExGpmAway = math.exp(1 / paramA * (-ratingDiff + paramB)) / minutes
    return ExGpmHome, ExGpmAway


def calcP(ExGpmHome, ExGpmAway, minutes=90):
    maxGoals = 9
    pHome = 0
    pDraw = 0
    pAway = 0
    for gHome in range(maxGoals + 1):
        pGHome = poissonPMF(ExGpmHome * minutes, gHome)
        for gAway in range(maxGoals + 1):
            pGAway = poissonPMF(ExGpmAway * minutes, gAway)
            if gHome > gAway:
                pHome += pGHome * pGAway
            elif gHome == gAway:
                pDraw += pGHome * pGAway
            else:
                pAway += pGHome * pGAway
    return pHome, pDraw, pAway


def poissonPMF(lam, k):
    pmf = lam**k * math.exp(-lam) / math.factorial(k)
    return pmf


if __name__ == '__main__':
    print('MAIN!')
    # df = pd.read_csv('output_rev.csv')
    # df = calcRatingDiff(df)
    # df.to_csv('output_rev.csv', index=False)

import csv
import datetime

totalOutstandingPrincipal = 0.0

veryRiskyPercent = 0.0
riskyPercent = 0.0
kindaRiskyPercent = 0.0
safePercent = 0.0

_6to8Percent = 0.0
_8to10Percent = 0.0
_10to12Percent = 0.0
_12to14Percent = 0.0
_14to16Percent = 0.0
_16to18Percent = 0.0

portfolioTill6Months = 0.0
portfolioTill12Months = 0.0
portfolioTill18Months = 0.0
portfolioTill24Months = 0.0
portfolioTill24MonthsPlus = 0.0

dataList = []


class Data:
    def __init__(self, interestRate='', remainingTerm='', mintosRiskScore='', outstandingAmount='', investedAmount='', lateLoanExposure='', kayRiskScore=0, rowNumber=0):
        self.interestRate = interestRate
        self.remainingTerm = remainingTerm
        self.mintosRiskScore = mintosRiskScore
        self.outstandingAmount = outstandingAmount
        self.investedAmount = investedAmount
        self.lateLoanExposure = lateLoanExposure
        self.kayRiskScore = kayRiskScore
        self.rowNumber = rowNumber
    def __repr__(self):
        return (
            f'Data(interestRate={self.interestRate!r}, remainingTerm={self.remainingTerm!r}, '
            f'mintosRiskScore={self.mintosRiskScore!r}, outstandingAmount={self.outstandingAmount!r}, '
            f'investedAmount={self.investedAmount!r}, lateLoanExposure={self.lateLoanExposure!r}, kayRiskScore={self.kayRiskScore!r}, rowNumber={self.rowNumber!r})'
        )

def read_csv_columns(file_path, skip_header=False):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        if skip_header:
            next(reader, None)
        rowNumber = 0
        for row in reader:
            if(rowNumber == 0): 
                rowNumber += 1
                continue # Skip the header row

            interestRate = 0
            remainingTerm = 0
            mintosRiskScore = 0
            outstandingAmount = 0
            investedAmount = 0
            lateLoanExposure = 0
            kayRiskScore = 0
            
            # row is now a list split by ';'
            for col_index, value in enumerate(row, start=1):
                match col_index:
                    case 4:
                        interestRate = float(value.replace(',', '.'))
                        if interestRate > 12.5: kayRiskScore += 1
                    case 5:
                        if(value == 'Late'): remainingTerm = 0.0
                        else: remainingTerm = float(value)
                    case 13:
                        mintosRiskScore = float(value.replace(',', '.'))
                        if mintosRiskScore < 7: kayRiskScore += 1
                    case 15:
                        outstandingAmount = float(value.replace(',', '.'))
                        global totalOutstandingPrincipal # to look up the global variable
                        totalOutstandingPrincipal += outstandingAmount
                    case 16:
                        investedAmount = float(value.replace(',', '.'))
                    case 24:
                        lateLoanExposure = float(value.replace(',', '.'))
                        if lateLoanExposure > 50: kayRiskScore += 3 
                        elif lateLoanExposure != 0: kayRiskScore += 1
                    case _:
                        continue
            data = Data(
                interestRate=interestRate,
                remainingTerm=remainingTerm,
                mintosRiskScore=mintosRiskScore,
                outstandingAmount=outstandingAmount,
                investedAmount=investedAmount,
                lateLoanExposure=lateLoanExposure,
                kayRiskScore=kayRiskScore,
                rowNumber=rowNumber+1
            )
            #print(f'Row {rowNumber}: {data}')
            dataList.append(data)
            rowNumber += 1
    print('Columns read successfully.')



read_csv_columns('Data.csv', skip_header=False)

def calculateRiskAmount():
    global veryRiskyPercent, riskyPercent, kindaRiskyPercent, safePercent, totalOutstandingPrincipal
    totalData = len(dataList)
    if totalData == 0:
        print('No data to calculate percentages.')
        return

    veryRiskyAmount = 0.0
    riskyAmount = 0.0
    kindaRiskyAmount = 0.0
    safeAmount = 0.0
    for data in dataList:
        #print(data)
        if data.kayRiskScore >= 3:
            veryRiskyAmount += data.outstandingAmount
        elif data.kayRiskScore == 2:
            riskyAmount += data.outstandingAmount
        elif data.kayRiskScore == 1:
            kindaRiskyAmount += data.outstandingAmount
        else:
            safeAmount += data.outstandingAmount

    veryRiskyPercent = (veryRiskyAmount / totalOutstandingPrincipal) * 100
    riskyPercent = (riskyAmount / totalOutstandingPrincipal) * 100
    kindaRiskyPercent = (kindaRiskyAmount / totalOutstandingPrincipal) * 100
    safePercent = (safeAmount / totalOutstandingPrincipal) * 100

calculateRiskAmount()

def calculatePortfolioRange():
    global _6to8Percent, _8to10Percent, _10to12Percent, _12to14Percent, _14to16Percent, _16to18Percent, totalOutstandingPrincipal
    
    totalData = len(dataList)
    if totalData == 0:
        print('No data to calculate percentages.')
        return
    
    _6to8PercentAmount = 0.0
    _8to10PercentAmount = 0.0
    _10to12PercentAmount = 0.0
    _12to14PercentAmount = 0.0
    _14to16PercentAmount = 0.0
    _16to18PercentAmount = 0.0

    for data in dataList:
        if data.interestRate >= 0.0 and data.interestRate <8.0: 
            _6to8PercentAmount += data.outstandingAmount
        elif data.interestRate >= 8.0 and data.interestRate <10.0:
            _8to10PercentAmount += data.outstandingAmount
        elif data.interestRate >= 10.0 and data.interestRate <12.0:
            _10to12PercentAmount += data.outstandingAmount
        elif data.interestRate >= 12.0 and data.interestRate <14.0:
            _12to14PercentAmount += data.outstandingAmount
        elif data.interestRate >= 14.0 and data.interestRate <16.0:
            _14to16PercentAmount += data.outstandingAmount
        elif data.interestRate >= 16.0 and data.interestRate <18.0:
            _16to18PercentAmount += data.outstandingAmount

    _6to8Percent = (_6to8PercentAmount / totalOutstandingPrincipal) * 100
    _8to10Percent = (_8to10PercentAmount / totalOutstandingPrincipal) * 100
    _10to12Percent = (_10to12PercentAmount / totalOutstandingPrincipal) * 100
    _12to14Percent = (_12to14PercentAmount / totalOutstandingPrincipal) * 100
    _14to16Percent = (_14to16PercentAmount / totalOutstandingPrincipal) * 100
    _16to18Percent = (_16to18PercentAmount / totalOutstandingPrincipal) * 100

calculatePortfolioRange()

def calculatePortfolioTerm():
    global portfolioTill6Months, portfolioTill12Months, portfolioTill18Months, portfolioTill24Months, portfolioTill24MonthsPlus, totalOutstandingPrincipal
    
    totalData = len(dataList)
    if totalData == 0:
        print('No data to calculate percentages.')
        return
    
    till6MonthsAmount = 0.0
    till12MonthsAmount = 0.0
    till18MonthsAmount = 0.0
    till24MonthsAmount = 0.0
    till24MonthsPlusAmount = 0.0

    for data in dataList:
        if data.remainingTerm >= 0.0 and data.remainingTerm <6.0: 
            till6MonthsAmount += data.outstandingAmount
        elif data.remainingTerm >= 6.0 and data.remainingTerm <12.0:
            till12MonthsAmount += data.outstandingAmount
        elif data.remainingTerm >= 12.0 and data.remainingTerm <18.0:
            till18MonthsAmount += data.outstandingAmount
        elif data.remainingTerm >= 18.0 and data.remainingTerm <24.0:
            till24MonthsAmount += data.outstandingAmount
        elif data.remainingTerm >= 24.0:
            till24MonthsPlusAmount += data.outstandingAmount

    portfolioTill6Months = (till6MonthsAmount / totalOutstandingPrincipal) * 100
    portfolioTill12Months = ((till12MonthsAmount + till6MonthsAmount) / totalOutstandingPrincipal) * 100
    portfolioTill18Months = ((till18MonthsAmount + till12MonthsAmount + till6MonthsAmount) / totalOutstandingPrincipal) * 100
    portfolioTill24Months = ((till24MonthsAmount + till18MonthsAmount + till12MonthsAmount + till6MonthsAmount) / totalOutstandingPrincipal) * 100
    portfolioTill24MonthsPlus = ((till24MonthsPlusAmount + till24MonthsAmount + till18MonthsAmount + till12MonthsAmount + till6MonthsAmount) / totalOutstandingPrincipal) * 100

calculatePortfolioTerm()

def write_file():
    global veryRiskyPercent, riskyPercent, kindaRiskyPercent, safePercent, totalOutstandingPrincipal
    global _6to8Percent, _8to10Percent, _10to12Percent, _12to14Percent, _14to16Percent, _16to18Percent
    global portfolioTill6Months, portfolioTill12Months, portfolioTill18Months, portfolioTill24Months, portfolioTill24MonthsPlus
    datetimeNow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fileName = 'Output__' + datetimeNow + '.txt'
    with open(fileName, 'w') as file:
        file.write(f'Total Outstanding Principal: \n')
        file.write(f'{totalOutstandingPrincipal} \n')
        file.write(f'\n')
        file.write(f'{str(veryRiskyPercent.__round__(2)).replace(".", ",")} :::::Very Risky: \n')
        file.write(f'{str(riskyPercent.__round__(2)).replace(".", ",")} :::::Risky: \n')
        file.write(f'{str(kindaRiskyPercent.__round__(2)).replace(".", ",")} :::::Kinda Risky: \n')
        file.write(f'{str(safePercent.__round__(2)).replace(".", ",")} :::::Safe: \n')
        file.write(f'----------------------------\n')

        file.write(f'\n')
        file.write(f'{str(_6to8Percent.__round__(2)).replace(".", ",")} :::::<8%\n')
        file.write(f'{str(_8to10Percent.__round__(2)).replace(".", ",")} :::::8-10%\n')
        file.write(f'{str(_10to12Percent.__round__(2)).replace(".", ",")} :::::10-12%\n')
        file.write(f'{str(_12to14Percent.__round__(2)).replace(".", ",")} :::::12-14%\n')
        file.write(f'{str(_14to16Percent.__round__(2)).replace(".", ",")} :::::14-16%\n')
        file.write(f'{str(_16to18Percent.__round__(2)).replace(".", ",")} :::::16-18%\n')
        file.write(f'<<<<<<<<<<<>>>>>>>>>>>>\n')
        file.write(f'{str(_6to8Percent.__round__(2)).replace(".", ",")}\n')
        file.write(f'{str(_8to10Percent.__round__(2)).replace(".", ",")}\n')
        file.write(f'{str(_10to12Percent.__round__(2)).replace(".", ",")}\n')
        file.write(f'{str(_12to14Percent.__round__(2)).replace(".", ",")}\n')
        file.write(f'{str(_14to16Percent.__round__(2)).replace(".", ",")}\n')
        file.write(f'{str(_16to18Percent.__round__(2)).replace(".", ",")}\n')
        file.write(f'----------------------------\n')

        file.write(f'\n')
        file.write(f'{str(portfolioTill6Months.__round__(2)).replace(".", ",")} :::::Till 6 Months: \n')
        file.write(f'{str(portfolioTill12Months.__round__(2)).replace(".", ",")} :::::Till 12 Months: \n')
        file.write(f'{str(portfolioTill18Months.__round__(2)).replace(".", ",")} :::::Till 18 Months: \n')
        file.write(f'{str(portfolioTill24Months.__round__(2)).replace(".", ",")} :::::Till 24 Months: \n')
        file.write(f'{str(portfolioTill24MonthsPlus.__round__(2)).replace(".", ",")} :::::Till 24 Months Plus: \n')
        file.write(f'----------------------------\n')

    print(f'Output written to {fileName}')

write_file()

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

def write_file():
    global veryRiskyPercent, riskyPercent, kindaRiskyPercent, safePercent, totalOutstandingPrincipal
    global _6to8Percent, _8to10Percent, _10to12Percent, _12to14Percent, _14to16Percent, _16to18Percent
    datetimeNow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fileName = 'Output__' + datetimeNow + '.txt'
    with open(fileName, 'w') as file:
        file.write(f'Total Outstanding Principal: \n')
        file.write(f'{totalOutstandingPrincipal} \n')
        file.write(f'\n')
        file.write(f'Very Risky: \n')
        file.write(f'Risky: \n')
        file.write(f'Kinda Risky: \n')
        file.write(f'Safe: \n')
        file.write(f'----------------------------\n')
        veryRiskyPercent = str(veryRiskyPercent.__round__(2)).replace('.', ',')
        riskyPercent = str(riskyPercent.__round__(2)).replace('.', ',')
        kindaRiskyPercent = str(kindaRiskyPercent.__round__(2)).replace('.', ',')
        safePercent = str(safePercent.__round__(2)).replace('.', ',')
        file.write(f'{veryRiskyPercent}\n')
        file.write(f'{riskyPercent}\n')
        file.write(f'{kindaRiskyPercent}\n')
        file.write(f'{safePercent}\n')

        file.write(f'\n')
        file.write(f'<8%: \n')
        file.write(f'8-10%: \n')
        file.write(f'10-12%: \n')
        file.write(f'12-14%: \n')
        file.write(f'14-16%: \n')
        file.write(f'16-18%: \n')
        file.write(f'----------------------------\n')
        _6to8Percent = str(_6to8Percent.__round__(2)).replace('.', ',')
        _8to10Percent = str(_8to10Percent.__round__(2)).replace('.', ',')
        _10to12Percent = str(_10to12Percent.__round__(2)).replace('.', ',')
        _12to14Percent = str(_12to14Percent.__round__(2)).replace('.', ',')
        _14to16Percent = str(_14to16Percent.__round__(2)).replace('.', ',')
        _16to18Percent = str(_16to18Percent.__round__(2)).replace('.', ',')
        file.write(f'{_6to8Percent}\n')
        file.write(f'{_8to10Percent}\n')
        file.write(f'{_10to12Percent}\n')
        file.write(f'{_12to14Percent}\n')
        file.write(f'{_14to16Percent}\n')
        file.write(f'{_16to18Percent}\n')

    print(f'Output written to {fileName}')

write_file()

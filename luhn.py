class LuhnAlgorithmImplementation:
    @staticmethod
    def get_odd_digits_from_right(ccn: str):
        odd_digits = []
        i = 1
        while i <= len(ccn):
            odd_digits.append(int(ccn[-i]))
            i += 2
        return odd_digits

    @staticmethod
    def get_doubled_even_digits_from_right(ccn: str):
        even_digits = []
        i = 2
        while i <= len(ccn):
            even_digits.append(int(ccn[-i]) * 2)
            i += 2
        return even_digits

    @staticmethod
    def perform_luhm_reduction_step(doubled_even_digits: list):
        reduced_even_digits = []
        for number in doubled_even_digits:
            if len(str(number)) == 2:
                reduced_number = int(str(number)[0]) + int(str(number)[1])
                reduced_even_digits.append(reduced_number)
            else:
                reduced_even_digits.append(number)
        return reduced_even_digits

    @staticmethod
    def perform_luhn_check(ccn: str):
        odd_digits = LuhnAlgorithmImplementation.get_odd_digits_from_right(ccn)
        even_digits = LuhnAlgorithmImplementation.get_doubled_even_digits_from_right(
            ccn
        )
        reduced_even_digits = LuhnAlgorithmImplementation.perform_luhm_reduction_step(
            even_digits
        )
        return (sum(odd_digits) + sum(reduced_even_digits)) % 10 == 0


valid_list = [
    "4929722788448974",
    "4532153527301093",
    "4123519983775289611",
    "2221006390645089",
    "2221002377565044",
    "2221009545948259",
    "374951985203704",
    "375657795995640",
    "377033005770199",
    "6011420417002296",
    "6011779819545586",
    "6011043383728500711",
    "3540132361941083",
    "3532943575896388",
    "3534572874835885659",
    "5586167521211357",
    "5552169349677223",
    "30336820891754",
    "30025596185653",
    "30507148408196",
    "36775929333792",
    "36962863771084",
    "36947801948571",
    "5020938312383108",
    "5020674605913604",
    "5893135547494438",
    "4508886190911942",
    "4917578207009779",
    "4508784955925761",
    "6384631770514045",
    "6381822961269787",
    "6372700004788289",
]

invalid_list = [
    "9605104549459978",
    "4215236901470724",
    "1673181029463829",
    "9549335963234978",
    "2773670812259396",
    "6734710524428492",
    "4852288526503654",
    "1072116585288028",
    "0067578639676344",
    "3328200094344990",
    "5552033345900049",
    "2582259086794603",
    "0254359184146060",
    "7335428198709517",
    "7906849230457216",
    "1497002913176116",
    "4282770540866628",
    "1233536009640176",
    "0638554039790807",
    "0392274947048528",
]

for num in valid_list:
    print(LuhnAlgorithmImplementation.perform_luhn_check(num))

for num in invalid_list:
    print(LuhnAlgorithmImplementation.perform_luhn_check(num))

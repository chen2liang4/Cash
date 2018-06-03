from LunarSolarConverter import LunarSolarConverter

converter = LunarSolarConverter.LunarSolarConverter()

for year in range(1971, 2071):
    solar = LunarSolarConverter.Solar(year, 8, 25)
    lunar = converter.SolarToLunar(solar)
    if lunar.lunarMonth == 7 and lunar.lunarDay == 4:
        print(year, year - 1971, year - 1948)

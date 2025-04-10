#-==@h1
# Dot Dictionary

#-== Makes a Python dictionary that can access keys
# with dot notation in addition to brackets ( /[] ).

#-------------------------------------------------
#-==@class
class DotDict(dict):
    #-== A Python dictionary that allows you to
    # access keys in dot notation style.

    #-== *Example:*
    #@codeblock
    # mycar = DotDict(
    #//    year = 2023,
    #//    make = 'Dodge',
    #//    model = 'Challenger',
    #//    trims = DotDict(
    #//        sport = DotDict(horsepower=256),
    #//        rt = DotDict(horsepower=425),
    #//        demon = DotDict(horsepower=712),
    #//    )
    # )
    #
    #-== print(mycar.year, mycar['model'], 
    #//         mycar.trims.rt.horsepower, 'hp')
    #@endcodeblock

    #-== *Output:* /-2023 Challenger 425 hp-/

    #-== Attributes can be accessed by dot notation,
    # as well as traditional bracket notation.
    # New attributes can only be added via bracket notation.
    # This essentially creates a dictionary that works like
    # a JavaScript Object.

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
            return
        raise AttributeError


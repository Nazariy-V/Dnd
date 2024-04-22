from dnd_character import Character, CLASSES

def create_character(stats,classs):
    with open("c_sheet.txt","w") as sheet:
        for i in stats:
            sheet.write(str(i)+"\n")
        sheet.write(classs)

def import_character():
    with open("c_sheet.txt","r") as sheet:
        stats=list(i.strip() for i in sheet.readlines())
    name,lvl,hp,strength,dexterity,constitution,wisdom,intelligence,charisma,clas=[i[1] if i[0]==0 or i[0]==9 else int(i[1]) for i in enumerate(stats)]
    return Character(name=name,
                     level=lvl,
                     max_hp=hp,
                     strength=strength,
                     dexterity=dexterity,
                     constitution=constitution,
                     wisdom=wisdom,
                     intelligence=intelligence,
                     charisma=charisma,
                     classs=CLASSES[clas])
import os
import shutil
import subprocess
import sys
import FreeSimpleGUI as psg

def digsiteOutput():
    text = open("newDigsiteSpawns.txt", "wt")
    text.close()
    text = open("newDigsiteSpawns.txt", "at")
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                point = int.from_bytes(r[0x54:0x58], "little")
                mapN = os.path.join(root, file).split("\\")[-2]
                mf = open("Map IDs.txt", "rt")
                lines = list(mf.read().split("\n")).copy()
                for t in lines:
                    if (t != ""):
                        nums = list(t.split(":")[0].replace(", ", ",").split(",")).copy()
                        for n in nums:
                            if (int(mapN.split(" [")[0]) == int(n)):
                                mapN = mapN + " [" + t.split(": ")[1] + "]"
                f = open("ff1_vivoNames.txt", "rt")
                vivoNames = [""] + list(f.read().split("\n")).copy()
                f.close()
                realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
                loc = point + 4
                while (realP[-1] > 0):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP = realP[0:-1]
                check = 0
                for val in realP:
                    index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (check == 0):
                            check = 1
                            text.write(mapN + ":\n")
                    text.write("\tZone " + str(index).zfill(2) + ":\n")
                    chip = int.from_bytes(r[(val + 8):(val + 12)], "little")
                    if (chip in [0x6F, 0x70, 0x71]):
                        chip = str(chip - 0x6F)
                    else:
                        chip = "?"
                    maxFos = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    text.write("\t\tFossil Chips Needed: " + chip + "\n")
                    text.write("\t\tMax Spawns: " + str(maxFos) + "\n")
                    numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                    point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                    for i in range(numSpawns):
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                        chance = int.from_bytes(r[(val + point4 + 4):(val + point4 + 8)], "little")
                        parts = [
                            int.from_bytes(r[(val + point4 + 16):(val + point4 + 20)], "little"),
                            int.from_bytes(r[(val + point4 + 20):(val + point4 + 24)], "little"),
                            int.from_bytes(r[(val + point4 + 24):(val + point4 + 28)], "little"),
                            int.from_bytes(r[(val + point4 + 28):(val + point4 + 32)], "little")
                        ]
                        s = "\t\t" + "[0x" + hex(val + point4).upper()[2:] + "] " + vivoNames[vivoNum] + ": " + str(chance) + "% "
                        s = s + "(Part 1: " + str(parts[0]) + "%, Part 2: " + str(parts[1]) + "%, Part 3: " + str(parts[2])
                        s = s + "%, Part 4: " + str(parts[3]) + "%)\n"
                        text.write(s)
                if (check == 1):
                    text.write("\n")
    text.close()

def messageReplace(fileNum, oldList, newList):
    byteList = []
    subprocess.run([ "fftool.exe", "./NDS_UNPACK/data/msg/msg_" + fileNum ])
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "rb")
    r = f.read()
    f.close()
    numStrings = int.from_bytes(r[4:8], "little")
    for i in range(12, 12 + (numStrings * 4), 4):
        loc = int.from_bytes(r[i:(i + 4)], "little")
        nextLoc = int.from_bytes(r[(i + 4):(i + 8)], "little")
        if ((i + 4) >= (12 + (numStrings * 4))):
            nextLoc = os.stat("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin").st_size
        temp = (r[(loc + 8):nextLoc]).decode("UTF-8", errors = "ignore")
        for j in range(min(len(oldList), len(newList))):
            temp = temp.replace(oldList[j], newList[j])
        temp = temp.encode("UTF-8", errors = "ignore")
        align = 4 - (len(r[loc:(loc + 8)] + temp) % 4)
        if (align < 4):
            byteList.append(r[loc:(loc + 8)] + temp + bytes(align))
        else:
            byteList.append(r[loc:(loc + 8)] + temp)
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "wb")
    f.close()
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "ab")
    f.write(r[0:16])
    writeLoc = int.from_bytes(r[12:16], "little")
    for i in range(len(byteList) - 1):
        writeLoc = writeLoc + len(byteList[i])
        f.write(writeLoc.to_bytes(4, "little"))
    for i in range(len(byteList)):
        f.write(byteList[i])
    f.close()
    subprocess.run([ "fftool.exe", "compress", "./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/", "-c", "None", "-c", "None",
        "-i", "0.bin", "-o", "./NDS_UNPACK/data/msg/msg_" + fileNum ])
    shutil.rmtree("NDS_UNPACK/data/msg/bin/")

def build_layout(swaps):
    f = open("ff1_vivoNames.txt", "rt")
    vivoNames = [""] + list(f.read().split("\n"))[:100].copy()
    f.close()

    new_layout = []
    for i, swap in enumerate(swaps):
        new_layout.append([
            psg.Text(f"Swap {i+1}:", size=8),
            psg.Combo(values=vivoNames, default_value=swap["v1"], key=f"swap_v1_{i}", enable_events=True),
            psg.Text("<===>"),
            psg.Combo(values=vivoNames, default_value=swap["v2"], key=f"swap_v2_{i}", enable_events=True)
        ])
    new_layout.append([ psg.Text("", size=32), psg.Button("Add Swap")])
    new_layout.append([ psg.Button("Run") ])
    return new_layout

def main():
    swaps = [{"v1": "", "v2": ""}]
    layout = build_layout(swaps)
    window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")
    good = 0
    while True:
        event, values = window.read()
        if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
            good = 0
            break
        elif "swap" in event:
            splits = event.split("_")
            swaps[int(splits[2])][splits[1]] = values[event]
        elif event == "Add Swap":
            swaps.append({"v1": "", "v2": ""})
            layout = build_layout(swaps)
            window.close()
            window = psg.Window("", layout, grab_anywhere=True, resizable=True, font="-size 12")
        elif (event == "Run"):
            good = 1
            break
        
    if (good == 1):
        vivos = list(range(0, 101))

        f = open("ff1_vivoNames.txt", "rt")
        vivoNames = [""] + list(f.read().split("\n"))[:100].copy()
        f.close()

        swapped = []
        for entry in swaps:
            if entry["v1"] != "" and entry["v2"] != "" and entry["v1"] != entry["v2"] and entry["v1"] not in swapped and entry["v2"] not in swapped:
                vivo1 = vivoNames.index(entry["v1"])
                vivo2 = vivoNames.index(entry["v2"])
                vivos[vivo1] = vivo2
                vivos[vivo2] = vivo1
                swapped.append(entry["v1"])
                swapped.append(entry["v2"])

        if (os.path.exists("NDS_UNPACK/y7.bin") == True):
            shutil.rmtree("./NDS_UNPACK/")
        if (os.path.exists("out.nds") == True):
            os.remove("out.nds")
        subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
        
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/data/episode/e0102", "output_e0102.xdelta",
            "NDS_UNPACK/data/episode/e0102x" ])
        os.remove("NDS_UNPACK/data/episode/e0102")
        os.rename("NDS_UNPACK/data/episode/e0102x", "NDS_UNPACK/data/episode/e0102") 
            
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/map/m" ])
        for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    f = open(os.path.join(root, file), "wb")
                    f.close()
                    f = open(os.path.join(root, file), "ab")
                    first = 0
                    mapN = os.path.join(root, file).split("\\")[-2]
                    numTables = int.from_bytes(r[0x50:0x54], "little")
                    point = int.from_bytes(r[0x54:0x58], "little")
                    realP = []
                    loc = point
                    for i in range(numTables):
                        realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                        loc = loc + 4
                    realP.append(len(r))
                    f.write(r[0:realP[0]])
                    for val in realP[0:-1]:
                        index = int.from_bytes(r[(val + 4):(val + 8)], "little")
                        if (index == 0):
                            f.write(r[val:realP[realP.index(val) + 1]])
                            continue
                        else:
                            f.write(r[val:(val + 8)])
                            f.write(r[(val + 8):(val + 16)])
                            f.write(r[(val + 16):(val + 0x2C)])
                            numSpawns = int.from_bytes(r[(val + 0x28):(val + 0x2C)], "little")
                            point3 = int.from_bytes(r[(val + 0x2C):(val + 0x30)], "little")
                            f.write(r[(val + 0x2C):(val + point3 + (numSpawns * 4))])
                            for i in range(numSpawns):
                                point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                                vivoNum = int.from_bytes(r[(val + point4):(val + point4 + 4)], "little")
                                f.write(vivos[vivoNum].to_bytes(4, "little"))
                                f.write(r[(val + point4 + 4):(val + point4 + 16)])
                                f.write(r[(val + point4 + 16):(val + point4 + 32)])
                                if (i == (numSpawns - 1)) and ((val + point4 + 32) < realP[realP.index(val) + 1]):
                                    f.write(r[(val + point4 + 32):realP[realP.index(val) + 1]])
                    f.close()
                    subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + mapN, "-i", "0.bin", "-o",
                        "NDS_UNPACK/data/map/m/" + mapN ])
        digsiteOutput()
        shutil.rmtree("NDS_UNPACK/data/map/m/bin/")
            
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode/e0899" ])
        f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0899/0.bin", "ab")
        parts = []
        for n in [51, 19, 80, 22]:
            head = ((vivos[n] - 1) * 4) + 1
            parts = parts + [head, head + 1, head + 2, head + 3]
        places = [0x10160, 0x10224, 0x102E8, 0x103AC, 0x10540, 0x10604, 0x106C8, 0x1078C, 0x10920, 0x109E4, 0x10AA8, 0x10B6C,
            0x10D00, 0x10DC4, 0x10E88, 0x10F4C, len(r)]
        f.write(r[0:places[0]])
        for i in range(16):
            f.write(parts[i].to_bytes(2, "little"))
            f.write(r[(places[i] + 2):places[i + 1]])
        f.close()
        
        f = open("ff1_vivoNames.txt", "rt")
        vivoNames = [""] + list(f.read().split("\n")).copy()
        f.close()
        text = open("newDPVivos.txt", "wt")
        text.close()
        text = open("newDPVivos.txt", "at")
        for n in [51, 19, 80, 22]:
            text.write(vivoNames[n] + " --> " + vivoNames[vivos[n]] + "\n")
        text.close()
        
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode/e1155" ])
        f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e1155/0.bin", "ab")
        head = ((vivos[98] - 1) * 4) + 1
        parts = [head, head + 1, head + 2, head + 3]
        places = [0x0F63C, 0x0F98C, 0x0FAC8, 0x0FC04, len(r)]
        f.write(r[0:places[0]])
        for i in range(4):
            f.write(parts[i].to_bytes(2, "little"))
            f.write(r[(places[i] + 2):places[i + 1]])
        f.close()        

        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0899/",  "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e0899" ])
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e1155/",  "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e1155" ])
        shutil.rmtree("NDS_UNPACK/data/episode/bin/")
        
        f = open("ff1_vivoNames.txt", "rt")
        vivoNames = [""] + list(f.read().split("\n")).copy()
        f.close()
        oldDPList = []
        newDPList = []
        articleDict = {}
        for n in [51, 19, 80, 22, 98]:
            if (vivoNames[vivos[n]][0] in ["A", "E", "I", "O", "U"]):
                if (vivoNames[vivos[n]] != "U-Raptor"):
                    articleDict[str(n)] = "an"
            elif (vivoNames[vivos[n]] in ["F-Raptor", "M-Raptor"]):
                articleDict[str(n)] = "an"
            else:
                articleDict[str(n)] = "a"
        for n in [51, 19, 80, 22]:
            for p in ["(Head)", "(Body)", "(Arms)", "(Legs)", "head", "body", "arms", "legs"]:
                oldDPList.append(vivoNames[n] + " " + p)
                newDPList.append(vivoNames[vivos[n]] + " " + p)
                oldDPList.append("a " + vivoNames[n] + "-" + p)
                newDPList.append(articleDict[str(n)] + " " + vivoNames[vivos[n]] + "-" + p)
                oldDPList.append("an " + vivoNames[n] + "-" + p)
                newDPList.append(articleDict[str(n)] + " " + vivoNames[vivos[n]] + "-" + p)
        oldTrList = []
        newTrList = []
        for p in ["(Head)", "(Body)", "(Arms)", "(Legs)", "head", "body", "arms", "legs"]:
            oldTrList.append(vivoNames[98] + " " + p)
            newTrList.append(vivoNames[vivos[98]] + " " + p)     
            oldTrList.append("a " + vivoNames[98] + "-" + p)
            newTrList.append(articleDict[str(98)] + " " + vivoNames[vivos[98]] + "-" + p)
            oldTrList.append("an " + vivoNames[98] + "-" + p)
            newTrList.append(articleDict[str(98)] + " " + vivoNames[vivos[98]] + "-" + p)           
        messageReplace("0398", oldDPList, newDPList)
        messageReplace("1191", oldTrList, newTrList)
        
        subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
        subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
        psg.popup("You can now play out.nds!", font = "-size 12")

main()
from username import Username
import json
import os

os.system("")
os.system("cls")
os.system("title Karus V1 - swiss army knife of OSINT")

logo = f"""\033[35m \033[1m
                                           ▄ •▄  ▄▄▄· ▄▄▄  ▄• ▄▌.▄▄ ·
                                           █▌▄▌▪▐█ ▀█ ▀▄ █·█▪██▌▐█ ▀.   
                                           ▐▀▀▄·▄█▀▀█ ▐▀▀▄ █▌▐█▌▄▀▀▀█▄    
                                           ▐█.█▌▐█ ▪▐▌▐█•█▌▐█▄█▌▐█▄▪▐█   
                                           ·▀  ▀ ▀  ▀ .▀  ▀ ▀▀▀  ▀▀▀▀    
                                           
                                           
                                \033[96m“The internet has an infallible and durable memory.”

\033[0m"""

input_data = {
    "Module": None,
    "Username": None,
    "Webhook": None,
    "File": None
}

for name in input_data.keys():
    print(logo)
    input_data[name] = input(f"\033[35m \033[1m                                 {name}: \033[96m")
    os.system("cls")

print(logo)


target = Username(name=input_data["Username"], module=input_data["Module"])
target.run()
print(json.dumps(target.results, indent=4))

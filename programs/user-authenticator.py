from visual_tables import SqlHelper
from tables import table
from colorama import init
from encrypt import crpty
import json

init()  # initializes colorama for coloring the terminal
table_name = "usuarios"
sql = SqlHelper("maked.db", table_name, id='id', name='txtn', password='txtn')                     # creates the helper, so this code isnt too long
sql.create()                                                                                       # create the database if it isnt created,
                                                                                                   # or just pass if it does
sql.save_db()                                                                                      # save changes
sql.commit()                                                                                       # and commit

session = {}                                                                                       # sessions to export into React


while True:  # just an infinite loop

    opt = input(table(["pagina inicial"], [["entrar"], ["logar"], ["sair"]]) + "escolha um:\n")    # choose one
    if opt.lower().strip() == "entrar":                                                            # if the user wants to enter

        name = input("entre o nome de usuário:\n")                                                 # user's name
        if sql.has_in(name, "name"):                                                               # if the user's name is in the database

            print("\033[32mnome verificado! \033[0m")                                              # return to the user that it is verified
        else:

            print("\033[31mnome de usuário não existe ou escrito errado!\033[0m")                  # or its wrong
            continue                                                                               # and then do the loop again

        senha = input("entre a senha:\n")  # user's password
        db_pass = sql.get_columns_from_table("password", f"name = '{name}'")[0][0]                 # get the user's password in the table row of the
                                                                                                   # user's name

        if crpty(name, senha) == db_pass:                                                          # if the password the user send and the database's
                                                                                                   # passwords are equal:
            print("senhas batem")                                                                  # in this part the user is authenticated
            session = {"name": name, "senha": db_pass}                                             # so do whatever you want here
            with open("session.json", 'w') as file:
                json.dump(session, file, indent=4)

        else:
            print("\033[31musuario e senha não combinam ou foram escritos errado\033[0m")          # here either the password is not there or the
                                                                                                   # user wrote it wrong

    elif opt.lower().strip() == "logar":                                                           # else if the user wants to join

        while True:  # loop

            name = input("entre o novo nome de usuário: \n")                                       # user's name
            if sql.has_in(name, "name"):                                                           # if the user's name already exists

                print(f"\033[31mnome de usuário: {name}  já existe, coloque outro\033[0m")         # alert the user
                continue                                                                           # return to the loop
            else:

                print("\033[32mnome verificado! \033[0m")

            senah = input("coloque a senha:\n")                                                    # double password just for the user not wrtiting
            # one
            # wrong
            senha = input("entre a senha novamente\n")

            if senha == senah:  # if both are equal
                print('senhas combinam')
            else:
                print("\033[31msenhas não combinam\033[0m")
                continue

            conf = input(f"confirmar usuario: {name} senha: {'*' * len(senha)} (sim/nao)\n")       # just confirming
            if conf.lower().strip() == "sim":
                senha = crpty(name, senha)                                                         # encrypting the password for safety
                sql.write_db([name, senha])                                                        # wrtiting to the database both values
                sql.commit()
                sql.save_db()                                                                      # commiting and saving
            else:
                continue
            break
    elif opt.lower().strip() == "sair":                                                            # if the user wants to leave
        exit()                                                                                     # he/she leaves (obviously)

    else:
        print("\033[31mescolha uma opção correta\033[0m")
        opt = ""

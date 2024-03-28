#-----------------------------------------------------------------------
# runserver.py
# Authors: Libo Tan
# 
# Refactored from lecture code and A3 Assignment
#-----------------------------------------------------------------------


import argparse
import sys
import user_controller



def args_processing():
    parser = argparse.ArgumentParser(description=
    'The ECO100 application')
    parser.add_argument('port', metavar = "port", help = "the port at which the server should listen", nargs= 1)
    args = parser.parse_args()
    return args.port[0]

#----------------------------------------------------------------------

def main():
    args = args_processing() 
    port = args
    try:
        user_controller.app.run(host = '0.0.0.0', port = port, debug = True) 
    except Exception as ex:
        print("Error: ", ex)
        sys.exit(1)

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()
    
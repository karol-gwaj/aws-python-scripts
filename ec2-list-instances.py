import os, sys, getopt, pprint

from boto import ec2

def main(argv):
    region = "us-east-1"
    public_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
   
    try:
        opts, args = getopt.getopt(argv,"r:",["pk=","sk="])
    except getopt.GetoptError:
        print 'ec2-list-instances.py -r <region> -pk <public key> -sk <secret key>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-r':
            region = arg
        elif opt == '-pk':
            public_key = arg
        elif opt == '-sk':
            secret_key = arg

    try:

        client = ec2.connect_to_region(region, aws_access_key_id=public_key, aws_secret_access_key=secret_key)
        reservations = client.get_all_instances()

        for r in reservations:
            for i in r.instances:
                print_instance(i)


    except Exception as ex:
        print ex
        sys.exit(1)


def name(i):
    if 'Name' in i.tags:
        n = i.tags['Name']
    else:
        n = ''
    return n

def private_ip(i):
    ip = str(i.private_ip_address)
    
    if ip == 'None':
        ip = ''

    return ip

def public_ip(i):
    ip = str(i.ip_address)
    
    if ip == 'None':
        ip = ''

    return ip

def print_instance(i):
    print i.id + '\t' \
        + i.state + '\t' \
        + name(i) + '\t' \
        + i.instance_type + '\t' \
        + private_ip(i) + '\t' \
        + public_ip(i)

if __name__ == "__main__":
    main(sys.argv[1:])
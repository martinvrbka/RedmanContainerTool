import os
import paramiko
import platform

# Step 1: Connect to multidocker via SSH
def connect_to_multidocker(address, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(address, username=username, password=password)
    return ssh_client

# Step 2: Return a list of Docker containers
def list_docker_containers(ssh_client):
    _, stdout, _ = ssh_client.exec_command("docker ps")
    container_list = stdout.read().decode().split("\n")[1:-1]
    return container_list

# Step 3: Allow the user to select a Docker command
def select_docker_command():
    print("Select a Docker command:")
    print("1. start")
    print("2. stop")
    print("3. restart")
    print("4. logs")
    command = input()
    if command == "1":
        return "start"
    elif command == "2":
        return "stop"
    elif command == "3":
        return "restart"
    elif command == "4":
        return "logs"
    else:
        print("Invalid command. Try again.")
        select_docker_command()

# Step 4: Apply the selected Docker command on the specified container
def apply_docker_command(ssh_client, container_id, command):
    if command == "logs":
        _, stdout, _ = ssh_client.exec_command(f"docker {command} {container_id}")
        logs = stdout.read().decode()
        os_type = platform.system()
        if os_type == "Windows":
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{container_id}.log")
        elif os_type == "Linux" or os_type == "Darwin":
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{container_id}.log")
        else:
            print("Unsupported operating system.")
            return
        with open(filename, "w") as log_file:
            log_file.write(logs)
        print(f"Logs saved to {filename}")
    else:
        ssh_client.exec_command(f"docker {command} {container_id}")

if __name__ == "__main__":
    address = "10.10.2.100"
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    ssh_client = connect_to_multidocker(address, username, password)
    container_list = list_docker_containers(ssh_client)
    for i, container in enumerate(container_list):
        print(f"{i + 1}. {container}")
    selected_container = int(input("Select a container by number: ")) - 1
    container_id = container_list[selected_container].split()[0]
    command = select_docker_command()
    apply_docker_command(ssh_client, container_id, command)
    ssh_client.close()
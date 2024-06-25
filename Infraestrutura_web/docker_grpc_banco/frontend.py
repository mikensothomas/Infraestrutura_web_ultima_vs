import grpc
import messenger_pb2
import messenger_pb2_grpc

def send_message(stub, sender, content):
    response = stub.SendMessage(messenger_pb2.Message(sender=sender, content=content))
    print("Mensagem enviada com sucesso.")

def main():
    channel = grpc.insecure_channel('192.168.1.10:50051')
    stub = messenger_pb2_grpc.MessengerStub(channel)
    
    sender = input("Digite seu nome: ")
    while True:
        message = input("Digite sua mensagem (ou 's' para sair): ")
        if message.lower() == 's':
            break
        send_message(stub, sender, message)
    
    channel.close()

if __name__ == '__main__':
    main()

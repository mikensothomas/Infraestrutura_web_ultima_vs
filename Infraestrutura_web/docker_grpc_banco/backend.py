import grpc
from concurrent import futures
import messenger_pb2
import messenger_pb2_grpc
import psycopg2

# Configuração do banco de dados PostgreSQL
DB_HOST = 'banco'
DB_PORT = '5432'
DB_NAME = 'banco_grpc'
DB_USER = 'usuario'
DB_PASSWORD = '12345'

# Classe que implementa o serviço gRPC Messenger
class MessengerServicer(messenger_pb2_grpc.MessengerServicer):
    def SendMessage(self, request, context):
        # Obtém os dados da mensagem do cliente
        sender = request.sender
        content = request.content
                
        # Conecta ao banco de dados PostgreSQL
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Conexão com o banco de dados estabelecida com sucesso")
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return messenger_pb2.Empty()
        
        try:
            with conn.cursor() as cursor:
                print("\n")
                print("==============++++++++++++++++++++++=============")
                print("\n")
                print(f"Mensagem recebida do cliente {sender}: {content}.")
                sql = "INSERT INTO mensagem (nome, mensagens) VALUES (%s, %s)"
                cursor.execute(sql, (sender, content))
                conn.commit()
                print("\n")
                print("==============++++++++++++++++++++++==++++===========")
                print("\n")
                print("Mensagem inserida no banco de dados com sucesso")
        except psycopg2.Error as e:
            print(f"Erro ao inserir mensagem no banco de dados: {e}")
        finally:
            conn.close()
            print("==============++++++++++++++++++++++=============")
        
        # Retorna uma resposta vazia para o cliente
        return messenger_pb2.Empty()

# Função para iniciar o servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_MessengerServicer_to_server(MessengerServicer(), server)
    server.add_insecure_port('192.168.1.10:50051')
    server.start()
    print("Servidor conectado na porta 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

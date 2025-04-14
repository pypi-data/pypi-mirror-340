import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
import datetime

class MongoDBAsyncIntegration:
    def __init__(self, connection_string, db_name):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[db_name]

    async def inserir_documento(self, colecao, documento):
        """
        Insere um documento em uma coleção de forma assíncrona.
        
        Args:
            colecao: Nome da coleção
            documento: Documento a ser inserido
            
        Returns:
            ID do documento inserido
        """
        collection = self.db[colecao]
        try:
            # Verificar se a coleção existe
            colecoes = await self.db.list_collection_names()
            print(f"Inserindo em {colecao}. Coleções disponíveis: {colecoes}")
            
            # Tentar inserção
            resultado = await collection.insert_one(documento)
            
            # Verificar se foi realmente inserido
            if resultado.inserted_id:
                verificacao = await collection.find_one({"_id": resultado.inserted_id})
                if verificacao:
                    print(f"Documento inserido e verificado com ID: {resultado.inserted_id}")
                else:
                    print(f"ALERTA: Documento não encontrado após inserção!")
            
            return resultado.inserted_id
        except Exception as e:
            print(f"ERRO na inserção: {str(e)}")
            raise e

    async def buscar_documento(self, colecao, filtro, limit=None, sort=None):
        """
        Busca documentos em uma coleção com opções de filtro, limite e ordenação de forma assíncrona.
        
        Args:
            colecao: Nome da coleção
            filtro: Critérios de filtro para a busca
            limit: Número máximo de documentos a retornar
            sort: Lista de tuplas (campo, direção) para ordenação. Ex: [("created_at", -1)]
            
        Returns:
            Um documento se limit não for especificado, ou uma lista de documentos se limit for especificado.
            Retorna None se nenhum documento for encontrado.
        """
        collection = self.db[colecao]
        
        try:
            if sort:
                # Se tiver ordenação, usa cursor
                cursor = collection.find(filtro)
                
                # Valida e aplica ordenação
                if not isinstance(sort, list):
                    raise ValueError("O parâmetro sort deve ser uma lista de tuplas (campo, direção)")
                    
                cursor = cursor.sort(sort)
                
                if limit:
                    cursor = cursor.limit(limit)
                    return await cursor.to_list(length=limit)
                else:
                    # Tenta pegar o primeiro documento do cursor ordenado
                    return await cursor.to_list(length=1)
            else:
                # Se não tiver ordenação, usa find_one para um documento
                # ou find com limit para múltiplos documentos
                if limit:
                    cursor = collection.find(filtro).limit(limit)
                    return await cursor.to_list(length=limit)
                return await collection.find_one(filtro)
                
        except Exception as e:
            logging.error(f"Erro ao buscar documento: {str(e)}")
            return None

    async def buscar_todos_documentos(self, colecao, filtro=None, sort=None, limit=None):
        """
        Busca todos os documentos em uma coleção com opções de filtro, ordenação e limite de forma assíncrona.
        
        Args:
            colecao: Nome da coleção
            filtro: Critérios de filtro para a busca (opcional)
            sort: Lista de tuplas (campo, direção) para ordenação (opcional)
            limit: Número máximo de documentos a retornar (opcional)
            
        Returns:
            Lista de documentos encontrados
        """
        collection = self.db[colecao]
        try:
            # Usa filtro vazio se não for especificado
            query = filtro if filtro is not None else {}
            
            # Cria cursor base
            cursor = collection.find(query)
            
            # Aplica ordenação se especificada
            if sort:
                cursor = cursor.sort(sort)
            
            # Aplica limite se especificado
            if limit:
                cursor = cursor.limit(limit)
            
            # Converte cursor para lista de forma assíncrona
            # Define um tamanho grande o suficiente para pegar todos os documentos quando não há limite
            batch_size = limit if limit else 100000
            documentos = await cursor.to_list(length=batch_size)
            
            if not documentos:
                logging.warning(f"Nenhum documento encontrado na coleção {colecao}")
            
            return documentos
            
        except Exception as e:
            logging.error(f"Erro ao buscar documentos: {str(e)}")
            return []

    async def atualizar_documento(self, colecao, filtro, atualizacao):
        """
        Atualiza um documento que corresponde ao filtro de forma assíncrona.
        
        Args:
            colecao: Nome da coleção
            filtro: Critérios de filtro para atualização
            atualizacao: Dicionário com as atualizações a serem aplicadas
            
        Returns:
            Número de documentos atualizados
        """
        collection = self.db[colecao]
        resultado = await collection.update_one(filtro, {'$set': atualizacao})
        return resultado.modified_count

    async def atualizar_varios_documentos(self, colecao, filtro, atualizacao):
        """
        Atualiza múltiplos documentos que correspondem ao filtro de forma assíncrona.
        
        Args:
            colecao: Nome da coleção
            filtro: Critérios de filtro para atualização
            atualizacao: Dicionário com as atualizações a serem aplicadas
            
        Returns:
            Número de documentos atualizados
        """
        collection = self.db[colecao]
        if not isinstance(atualizacao, dict) or '$set' not in atualizacao:
            atualizacao = {'$set': atualizacao}
        resultado = await collection.update_many(filtro, atualizacao)
        return resultado.modified_count

    async def deletar_documento(self, colecao, filtro):
        """
        Deleta documentos que correspondem ao filtro de forma assíncrona.
        
        Args:
            colecao: Nome da coleção
            filtro: Critérios de filtro para deletar
            
        Returns:
            Número de documentos deletados
        """
        collection = self.db[colecao]
        try:
            resultado = await collection.delete_many(filtro)  # Usando delete_many para permitir deleção múltipla
            return resultado.deleted_count
        except Exception as e:
            logging.error(f"Erro ao deletar documentos: {str(e)}")
            return 0

    async def fechar_conexao(self):
        """Fecha a conexão com o MongoDB de forma assíncrona"""
        self.client.close() 
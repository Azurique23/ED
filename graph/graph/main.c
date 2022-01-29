#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "graph.h" 

int main(int argc, char *argv[])
{
    char c, *tmp; 
    char *gfilename = "grafo.txt", *logfilename = "grafo.log";// Variaveis com os valores padrões para o nome do arquivos texto utilizados para criar o grafo e criar o log
    VertexWrapper *result;// Resultado das operações com os grafos
    int64_t origin = 0; // Que guarda a origen que o usuário informa para as operaões com grafos

    // Esse FOR abaixo é para definir o gfilename e logfilename se forem passado por argumentos
    for(int i = 1; i < argc; i++){
        tmp = argv[i];
        if(strcmp(tmp, "--log") == 0)
        {

            switch(i){
                case 1:
                    if(argc > 2)
                        logfilename = argv[2];
                    if(argc > 3)
                        gfilename = argv[3];
                    break;
                case 2:
                    if(argc == 3)
                        logfilename = argv[1];
                    if(argc > 3)
                        gfilename = argv[3];
                    break;
            }
            break;
        } else if((i == 1 && argc < 3) || argc > 3) {
            gfilename = argv[i];
        } else if (i == 2){
            gfilename = argv[1];
            logfilename = argv[i];
            break;
        }

    }

    Graph *graph = GraphFromFile(gfilename); // Criar um grafo apartir de arquivo de texto
    SetLogfile(logfilename); // Seta qual o nome do arquivo de saida dos logs
    do{
        if(origin){
            // Dijkstra
            result = Dijkstra(graph, origin); // Chama o algoritimo de djikstra
            printf("%s", VertexWrapperToString(result, graph)); // Mostra o resultado do algoritimo de djikstra
            ClearVertexWrappers(graph); // Libera a memória utilizada pelo vetex wrappers

            // Caminho Minimo em um DAO 
            result = ShortestPathDAG(graph, origin); // Chama o algoritimo do caminho minimo em um DAG
            printf("%s", VertexWrapperToString(result, graph)); // Printa o resultado do caminho minimo em um DAG 
            ClearVertexWrappers(graph);// Libera a memória utilizada pelo vetex wrappers
        }
        printf("Origem: ");
        scanf("%li", &origin); // Entrada para o usuário informa as origen que será utilizada nas operações

        while((c = getchar()) != '\n' && c != EOF); // Remove os espaço em branco do input 

    }while(origin);

    CloseLogfile(); // Fecha o arquivo de log

    return 0;
}


#include <stdint.h>

#define MAX_BUFFER_RESULT 2000
#define EMPTY_STRING ""
#define EMPTY_LIST_STRING "[]"

typedef char *String;

typedef struct sgraph Graph;
typedef struct svertex Vertex;
typedef struct sedge Edge;
typedef struct svertexwrapper VertexWrapper;

struct svertex{
    int64_t value;
    uint64_t degree; // É quantidade de arestas ligadas ao vértice 
    uint64_t indegree; // Quantidade de arestas direcionadas ao vértice
    uint64_t outdegree; // Quantidade de arestas que saem do vértice
    Edge *adjacencies; // lista de adjacências do vértice
    VertexWrapper *wrapper; 
};

struct sedge{
    int64_t weight;
    Vertex *tail; // Vértice onde a aresta inicia     
    Vertex *head; // Vértice onde a aresta termina
    Edge *next; // Próxima aresta na lista adjacências de um vertice
    Edge *anext; // Próxima aresta na lista adjacências do grafo 
};

struct sgraph{
    uint64_t size; // Número de arestas no grafo
    uint64_t maxorder; // Número máximo vértices no grafo
    uint64_t order; // Número de vértices no grafo
    Edge *adjacencies;
    Vertex *vertices;
};

struct svertexwrapper{
    int64_t distance;
    uint64_t level;
    uint64_t visited;
    Vertex *vertex; 
    Edge *preedge; // Aresta com predecessor 
    VertexWrapper *previous;
    VertexWrapper *next;
};

// Cria um novo grafo para de tamanho maximo maxorder e retorna o ponteiro para o grafo 
Graph *CreateGraph(uint64_t maxorder);

// Cria um grafo a partir de um arquivo de texto e retorna o ponteiro para o grafo 
Graph *GraphFromFile(const char *filename);

// Adiciona um novo vertice ao grafo e retorna o ponteiro para o vértice 
Vertex *AddVertex(Graph *graph, int64_t value);

// Adiciona uma nova aresta ao grafo e retorna o ponteiro para a aresta 
Edge *AddEdge(Graph *graph, int64_t tvalue, int64_t hvalue, int64_t weight);

// Cria um nova aresta e retorna o ponteiro para a aresta
Edge *CreateEdge(Vertex *tail,Vertex *head, int64_t weight);

// Faz a busca em profundidade no Grafo e retorna o ponteiro para lista de VertexWrapper com o resultado
VertexWrapper *DepthFirstSearch(Graph *graph, int64_t origin);

// Função auxiliar para o DepthFirstSearch 
void DFS(Edge *e, VertexWrapper **Q);

// Executa o algoritimo Dikstra no digrafo e retorna o ponteiro para a lista VertexWrapper com o resultado
VertexWrapper *Dijkstra(Graph *graph, int64_t origin);

// Wrapp os vértices e retorna o ponteiro para a lista dos wrappers 
VertexWrapper *InitializeGraph(Graph *graph, int64_t origin);

// Relaxa a aresta e deixa a lista wrappers ordena pela distancia
void RelaxEdgeDijkstra(Edge *e);

// Descobre o mais curto a partir do vértice vavalue em um DAG e retorna o ponteiro para a lista de VertexWrapper 
VertexWrapper *ShortestPathDAG(Graph *graph, int64_t origin);

// Relaxa a aresta em um DAG 
void RelaxEdgeDAG(Edge *e);

// Libera a memória de todos os wrappers criados 
void ClearVertexWrappers(Graph *graph);
    
// Retorna uma string com a representação do grafo ou NULL se grafo passado for um NULL pointer 
String GraphToString(Graph *graph);

// Retorna uma string com uma representação do resulta de uma lista VertexWrapper 
String VertexWrapperToString(VertexWrapper *wrappers, Graph *graph);

// Cria ou abre um arquivo para salvar o log
void SetLogfile(const String filename);

// Fecha o arquivo aberto para log 
int CloseLogfile();

// Cria uma nova coluna para o log de processamento 
void PutRowTable(VertexWrapper *cvw, VertexWrapper *Q, VertexWrapper *S);

// Cria a representação em forma de vetor a partir de uma lista de wrapper 
String VertexToStringList(VertexWrapper *vws);




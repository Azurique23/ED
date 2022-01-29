#include "stdlib.h"
#include "stdbool.h"
#include "stdio.h"
#include "limits.h"
#include "graph.h"


char buffer_result[MAX_BUFFER_RESULT];
FILE *logfile = NULL;

Graph *CreateGraph(uint64_t maxorder)
{
    Graph *graph;

    graph = (Graph *)calloc(1, sizeof(Graph));
    graph->vertices = (Vertex *)calloc(maxorder, sizeof(Vertex)); 
    graph->maxorder = maxorder;

    return graph;
}

Graph *GraphFromFile(const char *filename)
{
    FILE *fp;

    Graph *graph = NULL;
    uint64_t gmaxorder = 0;
    int64_t tvalue = 0, hvalue = 0, eweight = 0;

    if((fp = fopen(filename, "r")) == NULL){
        printf("Arquivo %s não existe.\n", filename);
        exit(EXIT_FAILURE);
    }

    fscanf(fp, "%lu\n", &gmaxorder);

    if(!gmaxorder){
        printf("Arquivo %s possui entrada(s) inválida(s).\n", filename);
        exit(EXIT_FAILURE);
    }

    graph = CreateGraph(gmaxorder);

    while(fscanf(fp, "%li %li %li\n", &tvalue, &hvalue, &eweight) != EOF)
    {
        if(!tvalue|| !hvalue|| !eweight){
            printf("Arquivo %s possui entrada(s) inválida(s).\n", filename);
            exit(EXIT_FAILURE);
        }
        AddEdge(graph, tvalue, hvalue, eweight);
        tvalue = hvalue = eweight = 0;
    };

    fclose(fp);

    return graph;
}

Vertex *AddVertex(Graph *graph, int64_t value)
{
    size_t i; 
    for(i = 0; i < graph->order; i++){
        if(graph->vertices[i].value == value)
            return graph->vertices+i;
    }

    if(graph->order >= graph->maxorder){
        printf("Grafo cheio.\n");
        exit(EXIT_FAILURE);
    }

    graph->vertices[graph->order++].value = value;

    return graph->vertices+i;
}

Edge *AddEdge(Graph *graph, int64_t tvalue, int64_t hvalue, int64_t weight)
{
    Vertex *tail = AddVertex(graph, tvalue);
    Vertex *head = AddVertex(graph, hvalue);
    Edge *edge = CreateEdge(tail, head, weight);

    graph->size++;
    tail->outdegree++;
    head->indegree++;
    edge->anext = graph->adjacencies;
    edge->next = tail->adjacencies;
    graph->adjacencies = edge;
    tail->adjacencies = edge;

    return edge;
}

Edge *CreateEdge(Vertex *tail, Vertex *head, int64_t weight)
{
    Edge *edge = (Edge *)malloc(sizeof(Edge));

    edge->weight = weight;
    edge->tail = tail;
    edge->head = head;

    return edge;
}

VertexWrapper *DepthFirstSearch(Graph *graph, int64_t origin)
{
    VertexWrapper *S = NULL, *Q = NULL, *tmp = NULL;
    Vertex *v;
    Edge *e;

    S = InitializeGraph(graph, origin);

    while(S){
        v = S->vertex;
        e = v->adjacencies;
        S->visited = 1;
        for(; e; e = e->next){
            if(e->head->wrapper->visited)
                continue;
            DFS(e, &Q);
        }

        if(S->next)
            S->next->previous = NULL;

        tmp = Q;
        Q = S;
        S = Q->next;
        Q->next = tmp;
        if(Q->next)
            Q->next->previous = Q;
    }
    return Q;
}

void DFS(Edge *edge, VertexWrapper **Q)
{
    Edge *e;
    Vertex *pre = edge->tail , *v = edge->head;  

    VertexWrapper *vw = v->wrapper;
    vw->distance = pre->wrapper->distance + edge->weight;
    vw->level = pre->wrapper->level + 1;
    vw->preedge = edge;

    e = v->adjacencies;

    vw->visited = true;
    for(; e; e = e->next){
        if(e->head->wrapper->visited)
            continue;
        DFS(e, Q);
    }

    if(vw->previous)
        vw->previous->next  = vw->next;

    if(vw->next)
        vw->next->previous = vw->previous;

    vw->previous = vw->next = NULL;
    
    vw->next = *Q;
    *Q = vw;
}

VertexWrapper *InitializeGraph(Graph *graph, int64_t origin)
{
    if(logfile) fprintf(logfile, "%s\n", __func__);
    size_t i;
    Vertex *v;
    VertexWrapper *wrappers = NULL, *vw, *ovw = NULL; 
    
    for(i = 0; i < graph->order; i++){
        v = &graph->vertices[i]; 
        vw = (VertexWrapper *)calloc(1, sizeof(VertexWrapper));
        vw->vertex = v; 
        v->wrapper = vw;
        if(v->value == origin){
            ovw = vw;
            continue;
        }
        vw->next = wrappers;
        if(vw->next)
            vw->next->previous = vw;
        wrappers = vw;
        vw->distance = INT_MAX;
    }

    if(ovw){
        ovw->next = wrappers;
        if(ovw->next)
            ovw->next->previous = ovw;
        wrappers = ovw;
        ovw->distance = 0;
    }
    else{
        printf("Origem %li não existe no grafo.\n", origin);
        return NULL;
    }
    return wrappers;
}

VertexWrapper *Dijkstra(Graph *graph, int64_t origin)
{
    if(logfile) fprintf(logfile, "%s\n", __func__);
    VertexWrapper *S, *Q, *T;
    Edge *e;

    S = Q = T = NULL;
    S = InitializeGraph(graph, origin);

    while(S)
    {
        PutRowTable(S, Q, S);
        e = S->vertex->adjacencies;
        for(;e ; e = e->next){
                RelaxEdgeDijkstra(e);
                PutRowTable(e->head->wrapper, Q, S);
            }

        if(T){
            T->next = S;
            S->previous = T;
        }else
            Q = S;
        T = S;
        S = T->next;
        T->next = NULL;
        if(S) S->previous = NULL;
    }
    PutRowTable(T, Q, S);
    if(logfile) {
        fprintf(logfile, "%s\n", VertexWrapperToString(Q, graph));
        fflush(logfile);
    }

    return Q;
}

void RelaxEdgeDijkstra(Edge *e)
{
    if(logfile) fprintf(logfile, "%s\n", __func__);
    VertexWrapper *tvw, *hvw, *tmpvw; // Wrapper da calda e da cabeça da aresta
    tvw = e->tail->wrapper;
    hvw = e->head->wrapper;
    if((tvw->distance + e->weight) < hvw->distance){
        hvw->distance = tvw->distance + e->weight;
        hvw->preedge = e;
        hvw->level = tvw->level+1;
        if(hvw->next){
            hvw->next->previous = hvw->previous;
        }
        hvw->previous->next = hvw->next;
        hvw->previous = NULL;
        hvw->next = NULL;
        tmpvw = tvw;
        while(tmpvw->next  && tmpvw->next->distance < hvw->distance){
            tmpvw = tmpvw->next;
        }

        if(tmpvw->next)
            tmpvw->next->previous = hvw;
        hvw->next = tmpvw->next;
        tmpvw->next = hvw;
        hvw->previous = tmpvw;
    }
}

VertexWrapper *ShortestPathDAG(Graph *graph, int64_t origin)
{
    if(logfile) fprintf(logfile, "%s\n", __func__);
    VertexWrapper *S, *Q, *tmp;
    Edge *e;

    S = Q = tmp = NULL;
    S = DepthFirstSearch(graph, origin);

    while(S)
    {
        PutRowTable(S, Q, S);
        e = S->vertex->adjacencies;
        for(;e ; e = e->next){
                RelaxEdgeDAG(e);
                PutRowTable(e->head->wrapper, Q, S);
            }
        tmp = Q;
        Q = S;
        S = Q->next;
        Q->next = tmp;
        if(S)
            S->previous = NULL;
    }

    PutRowTable(Q, Q, S);
    if(logfile) {
        fprintf(logfile, "%s\n", VertexWrapperToString(Q, graph));
        fflush(logfile);
    }

    return Q;
}

void RelaxEdgeDAG(Edge *e)
{
    if(logfile) fprintf(logfile, "%s\n", __func__);
    VertexWrapper *tvw, *hvw; // Wrapper da calda e da cabeça da aresta
    tvw = e->tail->wrapper;
    hvw = e->head->wrapper;
    if((tvw->distance + e->weight) < hvw->distance){
        hvw->distance = tvw->distance + e->weight;
        hvw->preedge = e;
        hvw->level = tvw->level+1;
    }
}

String GraphToString(Graph *graph)
{
    if(graph == NULL)
        return EMPTY_STRING;

    String repr; // String com a representação do grafo
    size_t si, vi; // Index do repr para manipulação da string, index para percorrer os vértices 

    Edge *e;
    Vertex v;

    repr = buffer_result;

    si = sprintf(repr, "\tORDEM: %lu\t|\t TAMANHO: %lu\n", graph->order, graph->size);
    si += sprintf(repr + si, "\n\tVértices\t|\t   Arestas\n");

    for(vi = 0; vi < graph->order && si < MAX_BUFFER_RESULT; vi++)
    {
        v = graph->vertices[vi];
        e = v.adjacencies;

        si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "\t   %li\t\t    ", v.value);

        if(e) for(; e->next; e = e->next)
            si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "%li - %li -> %li, ", v.value, e->weight, e->head->value);

        if(e)
            si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "%li - %li -> %li\n",v.value, e->weight, e->head->value);
    }

    return repr;
}

void ClearVertexWrappers(Graph *graph)
{
    for(int i = 0; i < graph->order; i++){
        free(graph->vertices[i].wrapper);
        graph->vertices[i].wrapper = NULL;
    }
}

String VertexWrapperToString(VertexWrapper *vws, Graph *graph)
{
    if(vws == NULL)
        return EMPTY_STRING;

    String repr; // String com a representação do grafo
    size_t si = 0, ei = 0; 

    VertexWrapper *w;
    Vertex *v;
    Edge *e;
    Edge *path[graph->order];

    repr = buffer_result;

    for(w = vws; w && si < MAX_BUFFER_RESULT; w = w->next)
    {
        v = w->vertex;
        si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "\n\t   VÉRTICE: %li\n", v->value );
        si += snprintf(repr+si, MAX_BUFFER_RESULT-si, " Distancia: %li   Nivel: %lu \n", w->distance, w->level);

        e = w->preedge;
        for(;e ; ei++, e = e->tail->wrapper->preedge)
            path[ei] = e;

        if(ei)si += snprintf(repr+si, MAX_BUFFER_RESULT-si, " origem: %li ", path[ei-1]->tail->value);
        else si += snprintf(repr+si, MAX_BUFFER_RESULT-si, " origem: %li ", v->value);
        for(; ei > 1; ei--){
            e = path[ei-1];
            si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "- %li -> %li ", e->weight, e->head->value);
        }
        if(ei){
            e = path[--ei];
            si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "- %li -> %li\n", e->weight, e->head->value);
        }
        si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "\n");
    }

    return repr;
}

void SetLogfile(const String filename)
{
    logfile = fopen(filename, "w+");
}

int CloseLogfile()
{
    int res = fclose(logfile);
    logfile = NULL;
    return res;
} 

void PutRowTable(VertexWrapper *cvw, VertexWrapper *Q, VertexWrapper *S)
{
    if(!logfile | !cvw)
        return;

    fprintf(logfile, "Vértices: %li ( ", cvw->vertex->value);
    if(cvw->distance != INT_MAX) fprintf(logfile, "%li, ",cvw->distance);
    else fprintf(logfile, "infinito, ");

    if(cvw->preedge) fprintf(logfile, "%li, ",cvw->preedge->tail->value );
    else fprintf(logfile, "origem, ");

    fprintf(logfile, "Q: %s, ", VertexToStringList(Q));
    fprintf(logfile, "S: %s )\n", VertexToStringList(S));
}

String VertexToStringList(VertexWrapper *vws)
{
    if(!vws)
        return EMPTY_LIST_STRING;

    if(vws == NULL)
        return EMPTY_STRING;

    String repr; // String com a representação do grafo
    size_t si = 0; 

    VertexWrapper *w;
    Vertex *v;

    repr = buffer_result;

    si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "[ ");
    for(w = vws; w->next && si < MAX_BUFFER_RESULT; w = w->next)
    {
        v = w->vertex;
        si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "%li, ", v->value );
    }
    v = w->vertex;
    si += snprintf(repr+si, MAX_BUFFER_RESULT-si, "%li ]", v->value );

    return repr;
}


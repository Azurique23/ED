#include "stdio.h"
#include "stdlib.h"
#include "time.h"

typedef unsigned char BYTE;

void printArray(int* a, size_t size)
{
    int i;
    printf("[ %d", a[0]);
    for (i = 1; i < size; i++)
    {
        printf(", %d", a[i]);
    }
    printf(" ]\n");
}

void swapElement(void* a, int i1, int i2, size_t n){
    size_t i;
    BYTE temp;
    BYTE* ca;
    ca = (BYTE *)a;
    i1 = i1*n; i2 = i2*n;

    for(i=0; i < n; i++) {
        temp = ca[i1+i];
        ca[i1+i] = ca[i2+i];
        ca[i2+i] = temp;
    }

}

void bubbleSort(int* a, size_t size)
{
    int i, j, temp;
    for (i = 0; i < size; i++){
        // printArray(a,size);
        for (j = 0; j < size-i-1; j++)
        {
            if (a[j] > *(a+j+1))
            {
                swapElement(a, j, j+1, sizeof(a[0]));
            }
        }
    }   
}

void selectionSort(int* a, size_t size)
{
    int i, j, lower;
    for(i = 0; i < size; i++){
        lower = i;
        for(j=i+1; j < size; j++){
            if(*(a+lower) > a[j]){
                lower = j;
            }
        }

        swapElement(a, i, lower, sizeof(a[0]));
    }

}

void insertSort(int* a, size_t size)
{
    int i, j, temp;

    for(i=1; i< size; i++){
        temp = a[i];
        for(j=i-1; j >= 0; j--){
            if(temp < *(a+j)){
                a[j+1] = a[j];
            }else{
                break;
            }
        }
        a[j+1] = temp;
    }
}

void quickSort(int* a, size_t size)
{
    
    short int hasJ = 0;
    int i, j, pivot;
    pivot = a[size-1];

    j = size-1;
    for(i = 0; i < size-1;i++)
    {
        if(!hasJ && pivot < a[i]){
            j = i;
            hasJ = 1;
        }else if(a[i] < pivot && hasJ){
            swapElement(a, j, i, sizeof(int));
            j++;
        }

    }

    a[size-1] = a[j];
    a[j] = pivot;

    if(j) quickSort(&a[0], j);
    if(j != size-1) quickSort(&a[j+1], size-j-1);

} 


int main()
{
    srand(time(NULL));
    unsigned short int size = 10;
    int a1[size], a2[size], a3[size], a4[size], a5[size], i, n;
    for(i = 0; i < size; i++){
        n= (rand()%100)+1;
        a1[i] = n;
        a2[i] = n;
        a3[i] = n;
        a4[i] = n;
        a5[i] = n;
    }
    printf("Start array: ");
    printArray(a1, size);

    bubbleSort(a1, size);
    printf("Bubble sort: ");
    printArray(a1, size);

    selectionSort(a2, size);
    printf("Selection sort: ");
    printArray(a2, size);

    insertSort(a3, size);
    printf("Insert sort: ");
    printArray(a3, size);

    quickSort(a4, size);
    printf("Quick sort: ");
    printArray(a4, size);


    return 0;
}
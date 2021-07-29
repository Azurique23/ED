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
    int i, j;
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
    int i, j, pivot;
    pivot = a[size-1];

    j = 0;
    for(i = 0; i < size-1;i++)
    {
        if(a[i] < pivot){
            swapElement(a, j, i, sizeof(int));
            j++;
        }
    }

    a[size-1] = a[j];
    a[j] = pivot;

    if(j) quickSort(&a[0], j);
    if(j != size-1) quickSort(&a[j+1], size-j-1);

} 

void mergeSort(int* a, size_t size)
{
    size_t i, j, k, mid;
    if(size > 2){
        mid = (size/2)+(size%2);
        mergeSort(&a[0], mid);
        mergeSort(&a[mid], size-mid);
        int la[mid];
        i = j =0;
        k = mid;
        for(i=0; i < mid; i++)
        {
            la[i] = a[i];
        }
        j = mid;
        i = k = 0;
        while (1)
        {
            if(k < mid && j < size){
                if(la[k] > a[j]){
                    a[i] = a[j];
                    j++;
                }else{
                    a[i] = la[k];
                    k++;
                }
                i++;
            }else if(k < mid){
                a[i] = la[k];
                k++;
                i++;
            }else{
                break;
            }
        }

        // for(i=mid; i < size;i++)
        // {
        //     for(j; j < i; j++){
        //         if(a[i] < a[j]){
        //             temp = a[i];
        //             for(x=i; x > j; x--) {a[x] = a[x-1];}
        //             a[j] = temp;   
        //             j++;
        //             break;
        //         }
        //     }
        // }

    }else if(size > 1){
        if(*(a) > *(a+1)){
            swapElement(a, 0, 1, sizeof(int));
        }
    }
}


int main()
{
    clock_t start, end;
    double delta;

    srand(time(NULL));

    size_t size = 70;
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

    mergeSort(a5, size);
    printf("Merge sort: ");    
    printArray(a5, size);


    for(int i = 0; i < size; i++)
    {
        if(a4[i] != a5[i] || a1[i] != a2[i] || a2[i] != a3[i] || a3[i] != a4[i]){
            printf("BS: %d, SS: %d, IS: %d, QS: %d, MS: %d ", a1[i], a2[i], a3[i], a4[i], a5[i]);
            break;
        }       
    }

    printf("END");

    return 0;
}
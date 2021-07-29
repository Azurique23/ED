#include "stdio.h"
#include "stdlib.h"

typedef unsigned char byte;

unsigned short int compare(byte *a, byte* data, size_t nb )
{
    size_t i;
    for(i=0; i < nb; i++)
    {
        if(a[i] != data[i]) return 0;
    }
    return 1;
}
int qCompare(const void* a, const void* b)
{
    return *((int*)a)- *((int*)b);
}

int simpleSearch(void* _a, size_t s, size_t nb, void* _data)
{
    size_t i;
    byte* a, *data;
    a = (byte* )_a;
    data = (byte*)_data;
    s *= nb;
    for(i=0; i < s; i+=nb)
    {
        if(compare(&a[i], data, nb)){
           return i/nb; 
        }
    }
    return -1;
}

int _binSearch(byte* a, size_t s, size_t nb, byte* data, size_t i)
{
    if(s > 1){
        size_t m, j;
        m = (s/2)+(s%2);
        j = m*nb;

        if(qCompare(data, a+j) >= 0){
            i += m; 
            _binSearch(a+j, s-m, nb, data, i);
        }else{
            _binSearch(a, m, nb, data, i);
        }


    }else
    {
        if(compare(a, data, nb)){
            return i;
        }
        return -1;
    }

}

int binarySearch(void* _a, size_t s, size_t nb, void* _data){
    byte* a,*data;
    a = (byte*)_a;
    data = (byte*)_data;
    qsort(a, s, nb, qCompare);
    _binSearch(a, s, nb, data, 0);
}


int main()
{
    int a[11] = {10, 2, 3, 8, 5, 6, 789878, 4, 9,23, 1};
    int data = 789878;
    printf("index de %d: %d\n",data, binarySearch(a, sizeof(a)/sizeof(a[0]),sizeof(data), &data));

    return 0;
}
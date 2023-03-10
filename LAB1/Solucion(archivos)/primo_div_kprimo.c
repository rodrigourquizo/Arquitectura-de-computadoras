#include <stdio.h>
#include <stdlib.h>

int num_es_primo(int num){
    int i;
    int cant_div=0;
    for(i=1;i<=num;i++){
        if(num%i==0)
            cant_div++;
    }
    //printf(" cant div = %d\n",cant_div);
    if(cant_div == 2)
        return 1;
    else
        return 0;
}

int num_divisible_k_primo(int num, int k){
    int i,j,cant_div_primo=0;
    for(i=1;i<=num;i++){
        if(num_es_primo(i)){
            if(num%i==0)
                cant_div_primo++;
        }
    }
    if(cant_div_primo == k)
        return 1;
    else    
        return 0;
}

int main(int argc, char const *argv[]){
    //Se piden 3 argumentos de entrada
    int a = atoi(argv[1]);
    int b = atoi(argv[2]);
    int c = atoi(argv[3]);
    //Numeros primos
    int num_en_rango=a;
    int num_primos_rango=0;
    int num_nums_div_k_primo=0;

    /*printf(" %d\n",a);
    printf(" %d\n",b);
    printf(" %d\n",c);*/

    //Numeros no primos divisibles por k-primos
    if (c==0){
        while(num_en_rango <= b){
            if(num_es_primo(num_en_rango))
                num_primos_rango++;
            num_en_rango++;
        }
        printf("Hay %d numeros primos", num_primos_rango);
    }
    else if(c>0){
        while(num_en_rango <= b){
            if(!num_es_primo(num_en_rango)){
                if(num_divisible_k_primo(num_en_rango,c))
                    num_nums_div_k_primo++;
            }
            num_en_rango++;
        }
        printf("Hay %d numeros divisibles por %d primo(s)", num_nums_div_k_primo, c);
    }
    
    return 0;
}
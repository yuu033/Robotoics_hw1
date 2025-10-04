// Do NOT change anything in this file
// You won't submit it anyway
#include <stdio.h>
#include "lib/cbmp.h"
#include "image_processing.h"
#include "game.h"

int main(){

    char path[128];

    printf("[OpenCV-Lite 1.0 Plays Tic-Tac-Toe]\n");
    printf("File Path to Process: ");
    scanf("%s", path);
    printf("Opening File %s...\n", path);

    Image image = open_image(path);

    while(1){
        // Menu Prompt
        printf("What would you like to do?\n");
        printf("0. Open another file\n");
        printf("1. Print Image in the Terminal\n");
        printf("2. Downscale\n");
        printf("3. Average Blurring\n");
        printf("4. Gaussian Blurring\n");
        printf("5. Edge Extraction\n");
        printf("6. Extract Tic-Tac-Toe Game\n");
        printf("7. Debug Mode\n");
        printf("8. Save Image\n");
        printf("9. Play Tic-Tac-Toe Interactively\n");
        printf("10. Exit\n");
        
        // Choose Prompt
        int option; int exit=0; 
        printf("Choose Option (0-10): ");
        scanf("%d", &option);

        // Handle Option
        switch(option){
            case 0:
                printf("File Path to Process: ");
                scanf("%s", path);
                image = open_image(path);
                break;
            case 1:
                asciiprint(image);
                break;
            case 2:
                while(1){
                    int f;
                    printf("Downscale Factor? ");
                    scanf("%d", &f);
                    if(image.width%f!=0){
                       printf("The image width (%d) is not divisible by %d\n", image.width, f);
                       continue; 
                    }
                    if(image.height%f!=0){
                       printf("The image height (%d) is not divisible by %d\n", image.width, f);
                       continue; 
                    }
                    image = downscale_image(image, f);
                    break;
                }
                break;
            case 3:
                while(1){
                    printf("Average kernel size: ");
                    int s;
                    scanf("%d", &s);
                    if(s <= 0){
                        printf("Kernel size should be greater than zero");
                        continue;
                    }
                    if(s > 25){
                        printf("Kernel size should be less then 25");
                        continue;
                    }
                    ConvKernel ker = generate_average_kernel(s);
                    image = convolve_image(image, ker);
                    break; 
                }
                break;
            case 4:
                while(0){} // to remove pedantic error of label should not be a part of a declaration
                int r; double s;
                while(1){
                    printf("Gaussian kernel radius: ");
                    scanf("%d", &r);
                    if(r <= 0){
                        printf("Kernel radius should be greater than zero");
                        continue;
                    }
                    if(r > 12){
                        printf("Kernel size should be less then or equal to 12 (because the maximum kernel size is 25)");
                        continue;
                    }
                    break;
                }
                while(1){
                    printf("Gaussian kernel stddev: ");
                    scanf("%lf", &s);
                    if(s <= 0){
                        printf("Kernel stddev should be greater than zero");
                        continue;
                    }
                    break;
                }
                ConvKernel ker = generate_gaussian_kernel(r, s);
                image = convolve_image(image, ker);
                break; 
            case 5:
                printf("Extracting edges...\n");
                image = extract_edges(image);
                break;
            case 6:
                printf("Extracting game...\n");
                if(image.height!=300 && image.width!=300){
                    printf("This feature only accepts images of size 300x300\n");
                    break;
                }
                Game game = extract_game(image);
                print_game(game);
                int result = report_winning_move(game);
                if(result == 0){
                    printf("There are no winning moves\n");
                }else if(result == 10){
                    printf("There are more than one winning moves\n");
                }else{
                    printf("Drawing on (%d,%d) will allow you to win\n", (result-1)/3, (result-1)%3);
                }
                break;
            case 7:
                printf("[DEBUG Mode]\n");
                printf("What would you like to do?\n");
                printf("1. Image Infodump\n");
                printf("2. Test Play Tic-Tac-Toe Function\n");
                printf("3. Average Kernel Generation \n");
                printf("4. Gaussian Kernel Generation \n");
                printf("5. Extract Game Test\n");
                printf("Choose Option (1-5): ");
                int x;
                scanf("%d", &x);
                if(x==1){
                    FILE *fptr;
                    fptr = fopen("dump.txt", "w");
                    fprintf(fptr, "%d\n", image.height);
                    fprintf(fptr, "%d\n", image.width);
                    for(int i=0; i<image.height; i++){
                        for(int j=0; j<image.width; j++){
                            fprintf(fptr, "%d %d %d\n", image.pixels[i][j].r,image.pixels[i][j].g, image.pixels[i][j].b);
                        }
                    }
                }else if(x==2){
                    printf("Insert 9 numbers for the tic-tac-toe [X:0, O:1, empty:2]:\n");
                    Game game; 
                    for(int i=0; i<3; i++){
                        for(int j=0; j<3; j++){
                            scanf("%d", &(game.grid[i][j]));
                        }
                    }
                    print_game(game);
                    int result = report_winning_move(game);
                    if(result == 0){
                        printf("There are no winning moves\n");
                    }else if(result == 10){
                        printf("There are more than one winning moves\n");
                    }else{
                        printf("Drawing on (%d,%d) will allow you to win\n", (result-1)/3, (result-1)%3);
                    }
                }else if(x==3){
                    printf("kernel size: ");
                    int x; scanf("%d", &x);
                    ConvKernel ker = generate_average_kernel(x);
                    for(int i=0; i<ker.size; i++){
                        for(int j=0; j<ker.size; j++){
                            printf("%.3lf ", ker.kernel[i][j]);
                        }
                        printf("\n");
                    }
                }else if(x==4){
                    printf("kernel radius: ");
                    int r; double s; scanf("%d", &r);
                    printf("kernel stddev: ");
                    scanf("%lf", &s);
                    ConvKernel x = generate_gaussian_kernel(r, s);
                    for(int i=0; i<x.size; i++){
                        for(int j=0; j<x.size; j++){
                            printf("%.3lf ", x.kernel[i][j]);
                        }
                        printf("\n");
                    }
                }else if(x==5){
                    if(image.height!=300 && image.width!=300){
                        printf("This feature only accepts images of size 300x300\n");
                        break;
                    }
                    Game game = extract_game(image);
                    print_game(game);
                }else{
                    printf("Invalid option!\n");
                }
                break;
            case 8:
                printf("Where to save (file name should end with .bmp)? ");
                char save_file_name[128] = "";
                scanf("%s", save_file_name);
                save_image(image, save_file_name);
                break;
            case 9:
                GameHistory gh; initialize_game_history(&gh);
                while(play_interactively(&gh)){}
                break;
            case 10:
                exit=1;
                break;
            default:
                printf("Invalid Option, try again?\n");
        }

        if(exit){ break; }

    }
}


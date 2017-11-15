#include <stdio.h>
#include <string.h>
#include <dirent.h> 


#define MAX_NUM_WORDS 200000
#define START_YEAR 2007
#define END_YEAR   2009
#define NUM_ARTS   7




char words[MAX_NUM_WORDS][16];
int  numwords[MAX_NUM_WORDS][12*(END_YEAR-START_YEAR)];
int  total_num_words;



void copy_word(char *w1,char *w2);
void add_word(char *w,int t_index);
int  find_pos(char *w,bool &found);



void print_table_all();
void print_table_RAW(int rep);
void print_table_labels();
void print_table_totals();

void print_table_quarterly();
void print_table_qrt(int rep);
void print_table_labels_qrt();
void print_table_totals_qrt();

void print_table_yearly();
void print_table_yr(int rep);
void print_table_labels_yr();
void print_table_totals_yr();


void print_table_monthly();
void print_table_mn(int rep);
void print_table_labels_mn();
void print_table_totals_mn();



bool good_word(char *w);
void process_file(char *filename,int year,int month);
void process_folder(int year,int month);








int main()
{
	total_num_words=0;
//	process_file("../fullarticlestext/2007_1/28pfizer.txt",2007,1);
//	return 0;
	for(int i=0;i<MAX_NUM_WORDS;i++)
		for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
			numwords[i][j]=0;

	for(int year=START_YEAR;year<END_YEAR;year++)
		for(int month=1;month<=12;month++)
			process_folder(year,month);
	char output_file[]="./RAW.txt";
	print_table_all();
	print_table_quarterly();
	print_table_yearly();
	print_table_monthly();
	return 0;
}

void process_folder(int year,int month)
{
	char parentfolder[200]="../fullarticlestext";
	DIR	*d;
	struct dirent *dir;	
	char folder[200];
	sprintf(folder,"%s/%d_%d",parentfolder,year,month);
	//printf("%s",folder);
	char filename[200];
	d = opendir(folder);
	int numfiles=0;
	printf("Now working on %d:%d -- files: [",year,month);
	if(d){
		while ((dir = readdir(d)) != NULL && numfiles < NUM_ARTS)
		      	if(strcmp(dir->d_name,"DATA.txt") && dir->d_name[strlen(dir->d_name)-1]=='t'){
				sprintf(filename,"%s/%s",folder,dir->d_name);
			        printf("%d ", numfiles);
				process_file(filename,year,month);
				numfiles++;
			}
		
		closedir(d);
	}
	printf("] Done! # of distinct words:%d \n", total_num_words);
	
	return ;
}


void process_file(char *filename,int year,int month)
{
	FILE *file;	
	file = fopen(filename,"r");
	char w[1000];
	int len;
	bool inpars=false;
	while (fscanf(file, "%s", w)!=EOF){
		len=strlen(w);
		if(w[len-1]==',' || w[len-1]=='.' || w[len-1]=='?' || w[len-1]==':' || w[len-1]==')')
			w[len-1]=0;	
		if(!strcmp(w,"PARAGRAPH"))
			inpars=true;
		else if (inpars)
			if(good_word(w))
				add_word(w,12*(year-START_YEAR)+month-1);
		//		printf("%s ",w);
	}
	fclose(file);	
	return ;
}

bool good_word(char *w)
{
	int i=0;
	while(w[i] && i<20){
		if(w[i]<='Z')
			w[i]+='a'-'A';
		if(w[i]<'a')
			return false;
		if(w[i]>'z')
			return false;
		i++;
	}
	if(i>15)
		return false;
	return true;
}




void add_word(char *w,int t_index)
{
//	printf("%s",w);
	if(!total_num_words){
		total_num_words++;
		copy_word(w,words[0]);
		numwords[0][0]=1;
		return ;
	}
	bool found;
	int pos=find_pos(w,found);
	if(found)
		numwords[pos][t_index]++;
	else{
		int t;
		for(int i=total_num_words;i>pos;i--){
			copy_word(words[i-1],words[i]);
			for(t=0;t<=t_index;t++)
				numwords[i][t]=numwords[i-1][t];
		}
		copy_word(w,words[pos]);
		for(t=0;t<t_index;t++)
			numwords[pos][t]=0;
		numwords[pos][t_index]=1;
		total_num_words++;
	}	
	return ;
}

void copy_word(char *w1,char *w2)
{
	int i=0;
	while(w1[i]){
		w2[i]=w1[i];
		i++;
	}
	w2[i]=0;
	return ;
}




int  find_pos(char *w,bool &found)
{
	int L=0;
	int R=total_num_words-1;
	int m;
	while(1<R-L){
		m=(R+L)/2;
		if(strcmp(words[m],w)<0)
			L=m;
		else
			R=m;
	}
	int LM=strcmp(words[L],w);
	int RM=strcmp(words[R],w);
//	printf("%s %s %s         LM %d      RM %d\n",words[m],words[L],words[R],LM,RM);	
	if(!LM){
		found=true;
		return L;
	}
	if(!RM){
		found=true;
		return R;
	}
	if(LM<0 && RM>0){
		found=false;
		return R;
	}
	if(strcmp(w,words[0])<0){
		found=false;
		return 0;
	}
//	if(strcmp(w,words[total_num_words-1])>0){
	found=false;
	return total_num_words;
//	}
}

/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
//Just printing from now
void print_table_monthly()
{
	print_table_mn(1);
	print_table_mn(2);
	print_table_mn(3);
	print_table_mn(5);
	print_table_mn(15);
	print_table_mn(30);
	print_table_mn(60);
	print_table_mn(100);
	print_table_mn(200);
	print_table_mn(500);
	print_table_mn(800);
	print_table_mn(1000);
	print_table_mn(1500);
	print_table_mn(2500);
	print_table_mn(4000);
	print_table_mn(8000);
	print_table_mn(12000);
	print_table_mn(20000);
	print_table_mn(40000);
	print_table_mn(80000);
	print_table_mn(120000);
	print_table_mn(200000);
	print_table_mn(400000);
	print_table_mn(1000000);
	print_table_mn(3000000);
	print_table_mn(10000000);
	print_table_labels_mn();
	print_table_totals_mn();
	return ;
}


void print_table_totals_mn()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Monthly_Total.txt");
	file=fopen(filename,"w");
	int sum;
	for(int j=0;j<12;j++){
		sum=0;
		for(int i=0;i<total_num_words;i++)
			for(int k=0;k<END_YEAR-START_YEAR;k++)
				sum+=numwords[i][j+12*k];
		fprintf(file,"%d\t",sum);
	
	}
	fclose(file);
	printf("Total number of words in each month are in the file: %s\n",filename); 
	return ;
}

void print_table_labels_mn()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Montly_Labels.txt");
	file=fopen(filename,"w");
		fprintf(file,"WordNumber\tWord\t");
		for(int mn=1;mn<=12;mn++)
				fprintf(file,"%d\t",mn);
		fprintf(file,"\n");
	fclose(file);
	printf("Monthly table data labels are in the file: %s\n",filename); 
	return ;
}




void print_table_mn(int rep)
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Monthly_Rep_%d.txt",rep);
	file=fopen(filename,"w");
	int sum;
	int counter=0;
	for(int i=0;i<total_num_words;i++){
		sum=0;
		for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
			sum+=numwords[i][j];
		if(sum>=rep){
			counter++;
			fprintf(file,"%-1d %-20s",counter,words[i]);
			for(int j=0;j<12;j++){
				sum=0;
				for(int k=0;k<END_YEAR-START_YEAR;k++)
					sum+=numwords[i][12*k+j];
				fprintf(file,"%-5d ",sum);
			}
			fprintf(file,"\n");
		}
	}
	fclose(file);
	printf("Monthly: Words that appeard at least %-10d times are now in the file: %s \n",rep,filename); 
	return ;
}

void print_table_yearly()
{
	print_table_yr(1);
	print_table_yr(2);
	print_table_yr(3);
	print_table_yr(5);
	print_table_yr(15);
	print_table_yr(30);
	print_table_yr(60);
	print_table_yr(100);
	print_table_yr(200);
	print_table_yr(500);
	print_table_yr(800);
	print_table_yr(1000);
	print_table_yr(1500);
	print_table_yr(2500);
	print_table_yr(4000);
	print_table_yr(8000);
	print_table_yr(12000);
	print_table_yr(20000);
	print_table_yr(40000);
	print_table_yr(80000);
	print_table_yr(120000);
	print_table_yr(200000);
	print_table_yr(400000);
	print_table_yr(1000000);
	print_table_yr(3000000);
	print_table_yr(10000000);
	print_table_labels_yr();
	print_table_totals_yr();
	return ;
}


void print_table_totals_yr()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Yearly_Total.txt");
	file=fopen(filename,"w");
	int sum;
	for(int j=0;j<(END_YEAR-START_YEAR);j++){
		sum=0;
		for(int i=0;i<total_num_words;i++)
			for(int k=0;k<12;k++)
				sum+=numwords[i][12*j+k];
		fprintf(file,"%d\t",sum);
	
	}
	fclose(file);
	printf("Total number of words in each year are in the file: %s\n",filename); 
	return ;
}

void print_table_labels_yr()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Yearly_Labels.txt");
	file=fopen(filename,"w");
		fprintf(file,"WordNumber\tWord\t");
		for(int year=START_YEAR;year<END_YEAR;year++)
			for(int qrt=1;qrt<=1;qrt++)
				fprintf(file,"%d\t",year);
		fprintf(file,"\n");
	fclose(file);
	printf("Yearly table data labels are in the file: %s\n",filename); 
	return ;
}




void print_table_yr(int rep)
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Yearly_Rep_%d.txt",rep);
	file=fopen(filename,"w");
	int sum;
	int counter=0;
	for(int i=0;i<total_num_words;i++){
		sum=0;
		for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
			sum+=numwords[i][j];
		if(sum>=rep){
			counter++;
			fprintf(file,"%-1d %-20s",counter,words[i]);
			for(int j=0;j<(END_YEAR-START_YEAR);j++){
				sum=0;
				for(int k=0;k<12;k++)
					sum+=numwords[i][12*j+k];
				fprintf(file,"%-5d ",sum);
			}
			fprintf(file,"\n");
		}
	}
	fclose(file);
	printf("Yearly: Words that appeard at least %-10d times are now in the file: %s \n",rep,filename); 
	return ;
}

void print_table_quarterly()
{
	print_table_qrt(1);
	print_table_qrt(2);
	print_table_qrt(3);
	print_table_qrt(5);
	print_table_qrt(15);
	print_table_qrt(30);
	print_table_qrt(60);
	print_table_qrt(100);
	print_table_qrt(200);
	print_table_qrt(500);
	print_table_qrt(800);
	print_table_qrt(1000);
	print_table_qrt(1500);
	print_table_qrt(2500);
	print_table_qrt(4000);
	print_table_qrt(8000);
	print_table_qrt(12000);
	print_table_qrt(20000);
	print_table_qrt(40000);
	print_table_qrt(80000);
	print_table_qrt(120000);
	print_table_qrt(200000);
	print_table_qrt(400000);
	print_table_qrt(1000000);
	print_table_qrt(3000000);
	print_table_qrt(10000000);
	print_table_labels_qrt();
	print_table_totals_qrt();
	return ;
}


void print_table_totals_qrt()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Quarterly_Total.txt");
	file=fopen(filename,"w");
	int sum;
	for(int j=0;j<4*(END_YEAR-START_YEAR);j++){
		sum=0;
		for(int i=0;i<total_num_words;i++)
			for(int k=0;k<3;k++)
				sum+=numwords[i][3*j+k];
		fprintf(file,"%d\t",sum);
	
	}
	fclose(file);
	printf("Total number of words in each quarter are in the file: %s\n",filename); 
	return ;
}

void print_table_labels_qrt()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Quarterly_Labels.txt");
	file=fopen(filename,"w");
		fprintf(file,"WordNumber\tWord\t");
		for(int year=START_YEAR;year<END_YEAR;year++)
			for(int qrt=1;qrt<=4;qrt++)
				fprintf(file,"%d_QRT%d\t",year,qrt);
		fprintf(file,"\n");
	fclose(file);
	printf("Quarterly table data labels are in the file: %s\n",filename); 
	return ;
}




void print_table_qrt(int rep)
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./Quarterly_Rep_%d.txt",rep);
	file=fopen(filename,"w");
	int sum;
	int counter=0;
	for(int i=0;i<total_num_words;i++){
		sum=0;
		for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
			sum+=numwords[i][j];
		if(sum>=rep){
			counter++;
			fprintf(file,"%-1d %-20s",counter,words[i]);
			for(int j=0;j<4*(END_YEAR-START_YEAR);j++){
				sum=0;
				for(int k=0;k<3;k++)
					sum+=numwords[i][3*j+k];
				fprintf(file,"%-5d ",sum);
			}
			fprintf(file,"\n");
		}
	}
	fclose(file);
	printf("Quarterly: Words that appeard at least %-10d times are now in the file: %s \n",rep,filename); 
	return ;
}



void print_table_all()
{
	print_table_RAW(1);
	print_table_RAW(2);
	print_table_RAW(3);
	print_table_RAW(5);
	print_table_RAW(15);
	print_table_RAW(30);
	print_table_RAW(60);
	print_table_RAW(100);
	print_table_RAW(200);
	print_table_RAW(500);
	print_table_RAW(800);
	print_table_RAW(1000);
	print_table_RAW(1500);
	print_table_RAW(2500);
	print_table_RAW(4000);
	print_table_RAW(8000);
	print_table_RAW(12000);
	print_table_RAW(20000);
	print_table_RAW(40000);
	print_table_RAW(80000);
	print_table_RAW(120000);
	print_table_RAW(200000);
	print_table_RAW(400000);
	print_table_RAW(1000000);
	print_table_RAW(3000000);
	print_table_RAW(10000000);
	print_table_labels();
	print_table_totals();
	return ;
}


void print_table_totals()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./ALL_Total.txt");
	file=fopen(filename,"w");
	int sum;
	for(int j=0;j<12*(END_YEAR-START_YEAR);j++){
		sum=0;
		for(int i=0;i<total_num_words;i++)
			sum+=numwords[i][j];
		fprintf(file,"%d\t",sum);
	
	}
	fclose(file);
	printf("Total number of words in each month are in the file: %s\n",filename); 
	return ;
}

void print_table_labels()
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./ALL_Labels.txt");
	file=fopen(filename,"w");
		fprintf(file,"WordNumber\tWord\t");
		for(int year=START_YEAR;year<END_YEAR;year++)
			for(int month=1;month<=12;month++)
				fprintf(file,"%d_%d\t",year,month);
		fprintf(file,"\n");
	fclose(file);
	printf("Table data labels are in the file: %s\n",filename); 
	return ;
}




void print_table_RAW(int rep)
{
	FILE *file;
	char filename[200];
	sprintf(filename,"./ALL_Rep_%d.txt",rep);
	file=fopen(filename,"w");
	int sum;
	int counter=0;
	for(int i=0;i<total_num_words;i++){
		sum=0;
		for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
			sum+=numwords[i][j];
		if(sum>=rep){
			counter++;
			fprintf(file,"%-1d %-20s",counter,words[i]);
			for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
				fprintf(file,"%-5d ",numwords[i][j]);
			fprintf(file,"\n");
		}
	}
	fclose(file);
	printf("Words that appeard at least %-10d times are now in the file: %s \n",rep,filename); 
	return ;
}













#include <stdio.h>
#include <math.h>
#include <string.h>
#include <dirent.h> 
#include <stdlib.h>

#define START_YEAR 2007
#define END_YEAR   2017
#define NUM_ARTS   700


double constp[10]=
{
0.1,//2007
0,//2008
0.7,//2009
0.7,//2010
0,//2011
0,//2012
1,//2013
0,//2014
0,//2015
0//2016
};

void process_folder(int year, int month);
class selected_words
{
	public:
		selected_words(char *filename,char *totalsfile, int num_ent);
		int total_num_words;
		void print_content();
		int find_word(char *w, double &score);
		void read_freqs(int pos,double *freq);
		~selected_words();
		int *totals;
		int num_entries;
		int **numwords;
		char **words;
		double *scores;
	private:
		void read(char *filename);		
		int  find_pos(char *w,bool &found);
		void set_totnumwords(char *filename);;
		double compute_score(int *rep);
		bool is_selected(int *rep);
};


class feature_vector
{
	public:
		feature_vector(selected_words *swd);
		~feature_vector();
		bool *vec;	
		void read(char *filename);
		void print();
		int total_words;
	private:
		selected_words *swd;
		bool good_word(char *w);
};



class naive_bayes
{
	public:
		int guess(feature_vector *fv,selected_words *sw);
	private:



};

int naive_bayes::guess(feature_vector *fv,selected_words *sw)
{
	double logp[sw->num_entries];
	double freq[sw->num_entries];
	int mindex=0;
	double maxl=logp[0];
	for(int i=0;i<sw->num_entries;i++)
		logp[i]=constp[i];
	for(int i=0;i<sw->total_num_words;i++)
		if(fv->vec[i]){
//			printf("\n %-15s",sw->words[i]);
			sw->read_freqs(i,freq);
			for(int j=0;j<sw->num_entries;j++){
				logp[j]+=log(freq[j]);
//				printf("%-16f",logp[j]);
			}
//			mindex=0;
//			maxl=logp[0];
//			for(int i=1;i<sw->num_entries;i++)
//				if(logp[i]>maxl){
//					maxl=logp[i];
//					mindex=i;
//			}
//			printf("-%d", mindex+2007);
	
			
		}
//	for(int i=0;i<10;i++)
//		printf("%d %f\n", i+2007, logp[i]);
	mindex=0;
	maxl=logp[0];
	for(int i=1;i<sw->num_entries;i++)
		if(logp[i]>maxl){
			maxl=logp[i];
			mindex=i;
		}
	return mindex;
}


int histo[10];

//COMMENTS: selects words. See the class definition above.
selected_words sw("./Yearly_Rep_800_editted.txt","./Yearly_Total.txt",10);
//COMMENTS: feature vector class. TRUE or FALSE depending on whether or not the word is in used in the file. 
feature_vector fvec(&sw);
//COMMENTS: naive bayes. It's actually just a function defined above.
naive_bayes nb;
//COMMENTS: counts the number of correctly categorized and incorrectly categorized articles in each year.
int result[10][2];

int main()
{
	for(int i=0;i<10;i++){
		histo[i]=0;
		result[i][0]=result[i][1]=0;
	}
	for(int year=2007;year<2017;year++)
		for(int month=1;month<12;month++)
			process_folder(year,month);
	for(int i=0;i<10;i++)
		printf("\n Year %d : percentage:%f   total number of articles  %d Number of articles predicted for this year  %d", i+2007, ((double)result[i][0])/((double)(result[i][0]+result[i][1])),result[i][0]+result[i][1],histo[i]);


	
	int tots=0;
	int tota=0;
	for(int i=0;i<10;i++){
		tots+=result[i][0];
		tota+=result[i][0]+result[i][1];
	}
	printf("\nFinal efficiency: %f", (double)tots/(double)tota);
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
	int guessy;
	printf("Now working on %d:%d -- files: [",year,month);
	if(d){
		while ((dir = readdir(d)) != NULL){
		      	if(numfiles>=NUM_ARTS && strcmp(dir->d_name,"DATA.txt") && dir->d_name[strlen(dir->d_name)-1]=='t'){
				sprintf(filename,"%s/%s",folder,dir->d_name);
				fvec.read(filename);
				if(fvec.total_words>400){
				       	guessy=nb.guess(&fvec,&sw)+2007; 
					if(guessy==year)
						result[year-2007][0]++;
					else
						result[year-2007][1]++;
					printf("ACTUAL YEAR: %d MY GUESS: %d FILENAME: %s \n",year,guessy, filename);
					histo[guessy-2007]++;
					//if(guessy==2007)
					//	return ;
				}
			}
			numfiles++;
		}
		
		closedir(d);
	}
	printf("]\n");
	return ;
}








/*




class naive_bayes
{
	public:
		char *filename;
		read_features();
	private:
			



};












int naive:bayes::read_features(char *filename)
{
//	printf("%s\n",filename);
//	return ;
	FILE *file;	
	file = fopen(filename,"r");
	char w[1000];
	int len;
	bool inpars=false;
	double p[10];
	double maxp;
	int year2;
	for(int i=0;i<10;i++)
		p[i]=0.0;
	while (fscanf(file, "%s", w)!=EOF){
		len=strlen(w);
		if(w[len-1]==',' || w[len-1]=='.' || w[len-1]=='?' || w[len-1]==':' || w[len-1]==')')
			w[len-1]=0;	
		if(!strcmp(w,"PARAGRAPH"))
			inpars=true;
		else if (inpars)
			if(good_word(w))
//				pr(w,p);	
//				printf("%s ",w);

	}
	fclose(file);	
	return ;

}











*/

//int main()
//{
/*	total_num_words=0;
	for(int i=0;i<MAX_NUM_WORDS;i++)
		for(int j=0;j<12*(END_YEAR-START_YEAR);j++)
			numwords[i][j]=0;

	read_file(500);
	for(int year=START_YEAR;year<END_YEAR;year++){
		
		for(int i=0;i<10;i++)
			yearsp[i]=0;
		for(int month=1;month<=12;month++)
			process_folder(year,month);
		for(int i=0;i<10;i++)
			printf("%d: %d\n",i+2007, yearsp[i]);
		printf("\n");

	}
*///	return 0;
//}
/*


	
void read_file(int rep)
{
	return ;
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



*/
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
selected_words::selected_words(char *filename,char *totalsfile, int num_ent)
{
	num_entries=num_ent;

	totals=new int [num_entries];
	FILE *file;
        file=fopen(totalsfile,"r");
	for(int i=0;i<num_entries;i++)
		fscanf(file,"%d", &totals[i]);
	fclose(file);
	

	read(filename);
}

int  selected_words::find_pos(char *w,bool &found)
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

int selected_words::find_word(char *w, double &score)
{
	bool found;
	int pos;
	pos=find_pos(w,found);
	if(!found)
		return -1;
	score=scores[pos];
	return pos;
}

void selected_words::read_freqs(int pos,double *freq)
{
	for(int i=0;i<num_entries;i++)
		freq[i]=((double) numwords[pos][i])/((double)totals[i]);
	return ;
}

void selected_words::print_content()
{
	for(int i=0;i<total_num_words;i++)
		printf("%d: %f %s\n", i, scores[i],words[i]); 
	return ;
}

selected_words::~selected_words()
{
	for(int row=0;row<total_num_words;row++){
		delete[] words[row];
		delete[] numwords[row];
	}
	
	delete[] words;
	delete[] numwords; 
	delete[] scores; 
}

void selected_words::set_totnumwords(char *filename)
{
	FILE *file;
//        char filename[200];
	char w[100];
  //      sprintf(filename,"./Yearly_Rep_%d.txt",minrep);
        file=fopen(filename,"r");
	total_num_words=0;
	int m;
	int rep[num_entries];
	
	while (w[0]!='a')
		fscanf(file,"%s", w);		
	for(int i=0;i<num_entries;i++)
		fscanf(file, "%d",&rep[i]);
	if(is_selected(rep))
		total_num_words++;
	
	while (fscanf(file, "%s", w)!=EOF){
		fscanf(file, "%s", w);
	//	strcpy(words[total_num_words],w);
		for(int i=0;i<10;i++)
			fscanf(file, "%d",&rep[i]);
		if(is_selected(rep))
			total_num_words++;
	}
	fclose(file);
	return ;
}


double selected_words::compute_score(int *rep)
{
	double score=0.0;
	int isum=0;
	int itv=0;
	for(int i=0;i<num_entries;i++){
		isum+=rep[i];
	}

	for(int i=0;i<num_entries-1;i++)
		itv+=abs(rep[i+1]-rep[i]);
//	sq/=10.0;
//	avg/=10.0;
//	score=(sq-avg*avg)/avg;
	double tv=(double)itv;
	double avg=((double)isum)/((double)num_entries);
	score=(log(avg))*tv/avg;
	return score;
}

bool selected_words::is_selected(int *rep)
{
	double score;
	score=compute_score(rep);
	bool selected;
	//////////////////
	selected=(score>=8)?true:false;
	//////////////////
	return selected;
}

void selected_words::read(char *filename)
{
	set_totnumwords(filename);	
	scores=new double[total_num_words];
	words=new char*[total_num_words];
	numwords=new int*[total_num_words];
	for(int row=0;row<total_num_words;row++){
		words[row] = new char[16];
		numwords[row]=new int[num_entries];
	}
	for(int i=0;i<total_num_words;i++)
		for(int j=0;j<num_entries;j++)
			numwords[i][j]=0;
	FILE *file;
 //       char filename[200];
	char w[100];
   //     sprintf(filename,"./Yearly_Rep_%d.txt",minrep);
        file=fopen(filename,"r");
	int rep[num_entries];
	int row=0;
	while (w[0]!='a')
		fscanf(file,"%s", w);		
	for(int i=0;i<num_entries;i++)
		fscanf(file, "%d",&rep[i]);
	if(is_selected(rep)){
		strcpy(words[row],w);
		for(int i=0;i<num_entries;i++)
			numwords[row][i]=rep[i];
		scores[row]=compute_score(rep);
		row++;
	}
	while (fscanf(file, "%s", w)!=EOF){
		fscanf(file, "%s", w);
	//	strcpy(words[total_num_words],w);
		for(int i=0;i<10;i++)
			fscanf(file, "%d",&rep[i]);
		if(is_selected(rep)){
			strcpy(words[row],w);
			for(int i=0;i<num_entries;i++)
				numwords[row][i]=rep[i];
			scores[row]=compute_score(rep);
			row++;
		}
	}
	fclose(file);
	return ;
}


















feature_vector::feature_vector(selected_words *swd2)
{
	swd=swd2;
	vec=new bool[swd->total_num_words];
	for(int i=0;i<swd->total_num_words;i++)
		vec[i]=false;
}

feature_vector::~feature_vector()
{
	delete[] vec;
}

void feature_vector::read(char *filename)
{
	total_words=0;
	FILE *file;     
        file = fopen(filename,"r");
        char w[1000];
        int len;
        bool inpars=false;
	double score;
	int pos;
	for(int i=0;i<swd->total_num_words;i++)
		vec[i]=false;
        while (fscanf(file, "%s", w)!=EOF){
                len=strlen(w);
                if(w[len-1]==',' || w[len-1]=='.' || w[len-1]=='?' || w[len-1]==':' || w[len-1]==')')
                        w[len-1]=0;     
                if(!strcmp(w,"PARAGRAPH"))
                        inpars=true;
                else if (inpars)
                        if(good_word(w)){
				total_words++;
				pos=swd->find_word(w,score);
				if(pos>=0)
					vec[pos]=true;
			}
						
        }
        fclose(file);   
	return ;
}

void feature_vector::print()
{
	for(int i=0;i<swd->total_num_words;i++){
		printf("%-20s", swd->words[i]);
		if(vec[i])
			printf(" 1\n");
		else
			printf(" 0\n");
	}
	return ;
}

bool feature_vector::good_word(char *w)
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




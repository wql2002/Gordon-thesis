/*
*              G O R D O N
* Detecting TCP variants on the internet
*---------------------------------------
*
*           Probe.c      : Base program. Registers nfqueue callback
*			Arguments    : <target>		URL of the target host
*					       <qd1>		First queuing delay to be emulated in us
*						   <qd2>        Second queuing delay to be emulated in us
*						   <trans-time> No. of packets after which the delay must be changed
*
*		    Example		 : sudo iptables -I INPUT -p tcp -s 137.132.83.98 -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
*						   ./prober www.facebook.com 5000 8000 1000
*/
#define OWD 125
#define DROPWINDOW 80
#define PRINTBUFF 0
#define true 1
#define false 0

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <linux/types.h>
#include <linux/netfilter.h>		
#include <libnetfilter_queue/libnetfilter_queue.h>
#include <linux/tcp.h>
#include <linux/ip.h>
#include <sys/time.h>
#include <sys/select.h>
#include <string.h>
#include <pthread.h>
#include <math.h>
#include <signal.h>

int drop = 1;
int acceptWindow = 0;
int dropWindow = 0;
uint dropSeq = 0;
int cap = 500;
int done = 0;
int emuDrop=10000;
uint32_t randomSeq=0;
int nextVal=0;
char buffSize[6];
int buff[250];
int indx = 0;

int ss=1;
int maxseq=0;

int dropped[200];

_Bool isRetrans( int seq ){
	int i=0;
	for(i=0; i<dropWindow; i++){
		if( seq == dropped[i])
			return 1;
	}
	return 0;
}

char* itoa(int n, char *number) 
{ 
	int digit, i=0, j=0, temp = n;
	i=0;
	if(n <= 0)
	{
		number[i]='0';
		return number;
	}
	while(temp!=0){
		digit = temp%10;
		number[i] = (char) (digit+48);
		temp /= 10;
		i++;
	}
	while(j<i/2){
		temp=number[j];
		number[j]=number[i-j-1];
		number[i-j-1]=temp;
		j++;
	} 
	return number;
} 

void split( char string[], int start, int end){
	char str[10];
	int i=0;
	for(i=0; i<(end-start); i++){
		str[i]=string[start+i];
	}
	strcpy(buffSize, str);
	return;
}

int getBuff(){
	char filename[] = "/proc/net/netfilter/nfnetlink_queue";
	FILE *file = fopen(filename, "r");

		fseek(file, 0, SEEK_SET);
		if (file != NULL) {
			char stats [60];
			fgets(stats,sizeof stats,file);
			split(stats, 12, 18); 
		}
	return atoi(buffSize);
}

void destroySession( struct nfq_handle *h, struct nfq_q_handle *qh ){
	nfq_destroy_queue(qh);

	#ifdef INSANE
		/* normally, applications SHOULD NOT issue this command, since
	 	* it detaches other programs/sockets from AF_INET, too ! */
		//printf("unbinding from AF_INET\n");
		nfq_unbind_pf(h, AF_INET);
	#endif

	nfq_close(h);
}

static int cb(struct nfq_q_handle *qh, struct nfgenmsg *nfmsg,
	      struct nfq_data *nfa, void *data)
{
	unsigned char *pkt;
	struct nfqnl_msg_packet_hdr *header;
	uint32_t id = 0;
	uint32_t tseq = 0;

	header = nfq_get_msg_packet_hdr(nfa);
	id = ntohl(header->packet_id);
	nfq_get_payload(nfa, &pkt);
	
	unsigned int by = 0;
	int i = 24;
	for (i = 24; i < 28; i++) {
		by = (unsigned int) pkt[i];
		tseq += by << 8*(24-i);
	}
	// printf("[NFQ][CB] tseq: %u\n", tseq);
	// printf("[NFQ][CB] randomSeq: %u\n", randomSeq);
	printf("[NFQ][CB] acceptWindow: %d\n", acceptWindow);
	// printf("[NFQ][CB] cap: %d\n", cap);
	// printf("[NFQ][CB] emuDrop: %d\n", emuDrop);
	// printf("[NFQ][CB] dropSeq: %d\n", dropSeq);
	
	// corner case: randomSeq = the first packet's tseq whose window
	// exceeds the `DROPWINDOW`, thus when we recerves its retrans packet,
	// we need to accept it to see the following trace.
	if(tseq == randomSeq){
		return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
	}
	else if(acceptWindow < cap){
		// emuDrop = window size that needs to be dropped to
		// check the retrans behavior.
		if(acceptWindow == emuDrop){
			ss=0;
			acceptWindow++;
			randomSeq = tseq;
			// printf("[NFQ][CB] case 1: NF_DROP\n");
			return nfq_set_verdict(qh, id, NF_DROP, 0, NULL);
		}
		else{
			acceptWindow++;
			// printf("[NFQ][CB] case 2: NF_ACCEPT\n");
			return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
		}
	}
	// if we receive the restran packet, we set the flag `done`,
	// stop experiment, and get the next receive window.
	else if( isRetrans(tseq) ){
		nextVal = acceptWindow + dropWindow;	
		done=1;
		// printf("[NFQ][CB] case 3: NF_ACCEPT\n");
		return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
	}
	// when `acceptWindow >= cap` && `not retrans`, get drop the packet,
	// and record the tseq of the dropped packets which will be used to
	// vefily the retrans packet.
	else{
		if(drop == 1){
			drop=0;
			dropSeq=tseq;
		}
		dropped[dropWindow] = tseq;
		dropWindow++;
		buff[dropWindow]=tseq;
		// printf("[NFQ][CB] case 4: NF_DROP\n");
		return nfq_set_verdict(qh, id, NF_DROP, 0, NULL);
	}
}

int getWinSize( char line[] ){
	char num[4];
	int i=0, j=0;
	for(i=0;i<6;i++){
		if(line[i]==' ')
			break;
	}
	for(j=0;j<4;j++){
		num[j]=line[i+j+1];
	}
	return atoi(num);
}

int main(int argc, char **argv)
{
	struct nfq_handle *h;
	struct nfq_q_handle *qh;
	int fd;
	int rv;
	char buf[4096] __attribute__ ((aligned));
	int lastWindow;
	int inputting = 0;

	char outfile[30] = "../Data/";
	strcat(outfile, argv[6]);
	strcat(outfile, "/windows.csv");
	printf("[DEBUG][multi-probe] output file: %s\n", outfile);
	FILE *ofile = fopen(outfile, "rw");

	int lastAccept = 0;

	char line [128]; 
    	while (fgets(line, sizeof line, ofile) != NULL) 
	{
		indx++; 
		lastWindow = atoi(line);
		printf("[DEBUG] lastWindow: %d\n", lastWindow);
		if(inputting==0){
			if(getWinSize(line)>DROPWINDOW){
				emuDrop = lastAccept;
				inputting=1;
			}
		}	
    		lastAccept = lastWindow;
	}
    	cap=atoi(line);
	if(cap==0){
		cap=lastWindow;
	}

	h = nfq_open();
	if (!h) {
		//fprintf(stderr, "error during nfq_open()\n");
		exit(1);
	}

	//printf("unbinding existing nf_queue handler for AF_INET (if any)\n");
	if (nfq_unbind_pf(h, AF_INET) < 0) {
		fprintf(stderr, "error during nfq_unbind_pf()\n");
		exit(1);
	}

	//printf("binding nfnetlink_queue as nf_queue handler for AF_INET\n");
	if (nfq_bind_pf(h, AF_INET) < 0) {
		fprintf(stderr, "error during nfq_bind_pf()\n");
		exit(1);
	}

	//printf("binding this socket to queue '0'\n");
	qh = nfq_create_queue(h,  0, &cb, NULL);
	if (!qh) {
		fprintf(stderr, "error during nfq_create_queue()\n");
		exit(1);
	}

	//printf("setting copy_packet mode\n");
	if (nfq_set_mode(qh, NFQNL_COPY_PACKET, 0xffff) < 0) {
		fprintf(stderr, "can't set packet_copy mode\n");
		exit(1);
	}

	fd = nfq_fd(h);
	int counter=0;
	
	/*
	argv[1] - target URL
	argv[2] - first delay
	argv[3] - second delay
	argv[4] - switch point
	*/

	int delay=atoi(argv[2]);
	int nextDelay=atoi(argv[3]);
	int switchPoint=atoi(argv[4]);

	signal(SIGCHLD, SIG_IGN);
	//Launch wget request in  a separate thread
	pid_t pid = fork();
	
	if(pid==0){
		//as desktop client 
		//char get[] ="wget -U 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0' -O /dev/null '";
		//as mobile client
		//char get[] ="wget -U 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.1' -O /dev/null '";
		char get[] ="wget -t 10 -T 45 -U 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0' -O indexPage --no-check-certificate ";
		strcat(get, argv[1]);
		// strcat(get, "\"");
		printf("%s\n", get);
		system(get);
		printf("=========DONE WITH WGET!");
		done = 1;
		destroySession(h, qh);
		exit(0);
	}
	else{
		int status = -1;

		while (done == 0 && (rv = recv(fd, buf, sizeof(buf), 0)) && rv >= 0){
			usleep(delay);
			printf("[NFQ] nfq_handle_packet begin ...\n");
			nfq_handle_packet(h, buf, rv);
			printf("[NFQ] nfq_handle_packet finished ...\n\n");
			if(counter>switchPoint) delay=nextDelay;
			counter++;
			status = kill(pid, 0);
			if (status == 0)
			{
				continue;
			}
			else{
				printf("\n\nWGET CHILD PROCESS HAS ENDED.\n\n");
				done=1;
				break;
			}
		}

		// // set some timeout params
		// int timeout_seconds = 5;
		// struct timeval timeout;
		// fd_set readfds;

		// FD_ZERO(&readfds); // 初始化文件描述符集合
		// FD_SET(fd, &readfds); // 添加套接字到集合

		// int max_fd = fd; // 假设fd是最大的文件描述符

		// while (done == 0) {
		// 	timeout.tv_sec = timeout_seconds;
    	// 	timeout.tv_usec = 0;

		// 	int ret = select(max_fd + 1, &readfds, NULL, NULL, &timeout);
		// 	if (ret == -1) {
		// 		printf("[WGET] select error...\n");
		// 		break;
		// 	} else if (ret == 0) {
		// 		printf("[WGET] timeout...\n");
		// 		break;
		// 	} else {
		// 		if (FD_ISSET(fd, &readfds)) {
		// 			rv = recv(fd, buf, sizeof(buf), 0);
		// 			if (rv >= 0) {
		// 				usleep(delay);
		// 				nfq_handle_packet(h, buf, rv);
		// 				if(counter>switchPoint) delay=nextDelay;
		// 				counter++;
		// 			}
		// 		}
		// 	}

		// 	status = kill(pid, 0);
		// 	if (status == -1) {
		// 		printf("\n\nWGET CHILD PROCESS HAS ENDED.\n\n");
		// 		done = 1;
		// 		break;
		// 	}
		// }

		printf("\n\n================================STATUS========: %d\n", status);

		destroySession(h, qh);

		if(done==-1)
			exit(0);

		fseek(ofile, 0, SEEK_END);

		if(PRINTBUFF && atoi(argv[5])==1){
			printf("-->%d\n", indx);
			int i = 0;
			for(i=0; i<dropWindow; i++){
				printf("\n%f %d", (indx*1.0)+(i*1.0/dropWindow), buff[i]);
			}
			printf("\n\n");
		}
			char number[5];
			char window[5];
			char in[5];
			char cmd[]="echo ";
			// printf("[DEBUG] nextVal: %d\n[DEBUG] nextVal-acceptWindow: %d\n", 
			// 	nextVal, nextVal-acceptWindow);
			//write data to windows.csv
			itoa(nextVal, number);
			strcat(cmd, number);
			strcat(cmd," ");
			itoa(nextVal-acceptWindow, window);
			strcat(cmd, window);
			strcat(cmd," ");
			itoa(indx, in);
			strcat(cmd, in);
			strcat(cmd, " >> ../Data/");
			strcat(cmd, argv[6]);
			strcat(cmd, "/windows");
			strcat(cmd, argv[5]);
			strcat(cmd, ".csv");
			system(cmd);
			printf("[DEBUG][CMD] %s\n", cmd);
	}	

	return 0; 
}

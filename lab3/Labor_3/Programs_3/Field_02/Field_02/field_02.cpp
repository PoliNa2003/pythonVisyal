
//строим картину линий электромагнитного поля


#define STRICT
#include <windows.h>
#include <windowsx.h>
#include <math.h>
#include <stdio.h>
#include <tchar.h>


//имя класса окна
WCHAR szClassName[] = L"LineClass";
//заголовок окна
WCHAR szWindowTitle[] = L"Korneev V.        "
			L"   Vector-Field,       "
			L"   rotation  by  mouse  and  keyboard (arrows)";


struct ANGLS {
	double fi, teta;
};

static ANGLS angl,anglOld;


//прототипы функций
BOOL RegisterApp(HINSTANCE hInst);
HWND CreateApp(HINSTANCE, int);
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void LineCreate();
void LineDestroy();
void LinePaint(HWND);
void LineLButtonDown(HWND,int,int);
void LineMouseMove(HWND,int,int);
void DrawBox(HWND, HDC, ANGLS);
void LineLButtonUp(HWND);
void PointCorns();


//главная функция
int PASCAL WinMain(HINSTANCE hInst,
						 HINSTANCE hPrevInstance,
						 LPSTR     lpszCmdParam,
						 int       nCmdShow)
{
	MSG msg;

	if(!RegisterApp(hInst))  //регистрация приложения
		return FALSE;

	if(!CreateApp(hInst,nCmdShow))  //создание окна приложения
		return FALSE;

	while(GetMessage(&msg,NULL,0,0))   //цикл обработки сообщений
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	return 0;
}

//регистрация класса окна 
BOOL RegisterApp(HINSTANCE hInst)
{
	WNDCLASS wc;

	wc.style         = CS_HREDRAW | CS_VREDRAW;
	wc.lpfnWndProc   = WndProc;
	wc.cbClsExtra    = 0;
	wc.cbWndExtra    = 0;
	wc.hInstance     = hInst;
	wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
	wc.hCursor		  = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = GetStockBrush(LTGRAY_BRUSH);
	wc.lpszMenuName  = (LPCTSTR)"APP_MENU";
	wc.lpszClassName = szClassName;

	return RegisterClass(&wc);
}



//создание окна
HWND CreateApp(HINSTANCE hInstance, int nCmdShow)
{
	 HWND hwnd;

	 hwnd = CreateWindow(szClassName,
									 szWindowTitle,
									 WS_OVERLAPPEDWINDOW,
									 100, 
									 30, 
									 700, 
									 700, 
									 NULL,
									 NULL,
									 hInstance,
									 NULL);

	if(hwnd == NULL)
		return hwnd;

	ShowWindow(hwnd,nCmdShow);
	UpdateWindow(hwnd);

	return hwnd;
}






//функция обработки сообщений  
LRESULT CALLBACK  WndProc(HWND hwnd, UINT msg,
											WPARAM wParam, LPARAM lParam)
{

	int x,y;
	switch(msg)
	{
		case WM_CREATE:
			LineCreate();
			break;

		case WM_PAINT:
			LinePaint(hwnd);
			break;

		case WM_LBUTTONDOWN:
				x = LOWORD(lParam);
				y = HIWORD(lParam);
				LineLButtonDown(hwnd,x,y);
			break;

		case WM_LBUTTONUP:
				LineLButtonUp(hwnd);
				InvalidateRect(hwnd,NULL,TRUE);
			break;


		case WM_MOUSEMOVE:
				x = LOWORD(lParam);
				y = HIWORD(lParam);

				LineMouseMove( hwnd,x,y);
			break;

		case WM_KEYDOWN:
			switch(wParam)
			{
				case VK_LEFT:
					angl.fi += 10;
					InvalidateRect(hwnd,NULL,TRUE);
					break;

				case VK_RIGHT:
					angl.fi -= 10;
					InvalidateRect(hwnd,NULL,TRUE);
					break;

				case VK_UP:
					angl.teta += 10;
					InvalidateRect(hwnd,NULL,TRUE);
					break;

				case VK_DOWN:
					angl.teta -= 10;
					InvalidateRect(hwnd,NULL,TRUE);
					break;
			}
			break;

		case WM_DESTROY:
			LineDestroy();
			break;

		default:
			return DefWindowProc(hwnd,msg,wParam,lParam);
	}

	return 0L;
}


double const M_PI = 3.141592654;

struct TDATA {
	BOOL ButtonDown;
	BOOL Drawing;
};

static TDATA Dat;


struct CORD {
	int x, y;
};

static CORD cor,corOld;

struct POINT3 {
	double x, y, z;
};

static POINT3 Point[8], PointB[32];

struct VECTORS {
	double x, y, z;
	double dx, dy, dz;
};

static VECTORS vect[32];

struct VECMAG {
	double hx, hy, hz;
};







//вершины магнитной пластинки
double Px[4], Py[4], Pz[4];

//размеры поля вывода в мировых координатах и в пикселях
double xe1, xe2, ye1, ye2;
int    ne1, ne2, me1, me2;

//длины координатных осей (в мировых координатах)
double xmax, ymax, zmax;

//размеры магнитной пластинки
double ax, ay;



//задаем различные параметры в начале работы приложения
void LineCreate()
{

//размеры поля вывода в мировых координатах и в пикселях
	xe1 = -3;  xe2 =   3; ye1 =  -3; ye2 =  3;
//	ne1 = 100; ne2 = 500; me1 = 450; me2 = 50;

//длины координатных осей (в мировых координатах)
	xmax=1.8, ymax=1.8, zmax=1.8;

//задаем вершины куба, связанного с подвижной системой координат
	PointCorns();


//размеры магнитной пластинки
	ax = xmax/2, ay = ymax/2;


//задаем вершины магнитной пластинки
	Px[0] =   ax;  Py[0] =   ay;  Pz[0] =  0.0;
	Px[1] =  -ax;  Py[1] =   ay;  Pz[1] =  0.0;
	Px[2] =  -ax;  Py[2] =  -ay;  Pz[2] =  0.0;
	Px[3] =   ax;  Py[3] =  -ay;  Pz[3] =  0.0;


//задаем начальные точки линий поля
	int i, j, k, N = 4 ,  M = 4;
	double x, y, dx = 2*ax/(N-1), dy = 2*ay/(M-1);
	double d = 0.1;

	for( i=0; i<N; i++)
	{
		x = -ax + dx*i;
		for(j=0; j<M; j++)
		{
			y = -ay + dy*j;
			k = j + 4*i;
			PointB[k].x = x;
			PointB[k].y = y;
			PointB[k].z = d;

			PointB[k+16].x = x;
			PointB[k+16].y = y;
			PointB[k+16].z = -d;
		}
	}


//начальные значения углов поворота системы координат
	angl.fi = 30; angl.teta = 60;
}


//задаем вершины куба, связанного с подвижной системой координат
void	PointCorns()
{
	Point[0].x =  xmax; Point[0].y =  ymax; Point[0].z = -zmax;
	Point[1].x = -xmax; Point[1].y =  ymax; Point[1].z = -zmax;
	Point[2].x = -xmax; Point[2].y = -ymax; Point[2].z = -zmax;
	Point[3].x =  xmax; Point[3].y = -ymax; Point[3].z = -zmax;
	Point[4].x =  xmax; Point[4].y =  ymax; Point[4].z = zmax;
	Point[5].x = -xmax; Point[5].y =  ymax; Point[5].z = zmax;
	Point[6].x = -xmax; Point[6].y = -ymax; Point[6].z = zmax;
	Point[7].x =  xmax; Point[7].y = -ymax; Point[7].z = zmax;
}


//вычисляем магнитное поле (hx,hy,hz) в заданной точке пространства (x,y,z)
VECMAG magn(double x, double y, double z)
{
	VECMAG mag;
	double s11, s12, s21, s22;
	double u1, u2, v1, v2;

	u1 = x - ax; u2 = x + ax;
	v1 = y - ay; v2 = y + ay;

	s11 = sqrt(u1*u1 + v1*v1 + z*z);
	s12 = sqrt(u1*u1 + v2*v2 + z*z);
	s21 = sqrt(u2*u2 + v1*v1 + z*z);
	s22 = sqrt(u2*u2 + v2*v2 + z*z);


	mag.hx =
			 log(((v1 + s21)/(v1 + s11))*((v2 + s12)/(v2 + s22)));
	mag.hy =
			 log(((u1 + s12)/(u1 + s11))*((u2 + s21)/(u2 + s22)));
	mag.hz =
			 atan((u2*v2)/(z*s22)) - atan((u1*v2)/(z*s12)) -
			 atan((u2*v1)/(z*s21)) + atan((u1*v1)/(z*s11));

	return mag;
}



void LineDestroy()
{
	PostQuitMessage(0);   //закрываем окно приложения
}



//угловые коэффициенты поворота системы координат
double sf,cf,st,ct;

//переход в видовую систему координат и ортографическое проецирование 
double Xe(double x,double y)
{
  return -sf*x+cf*y;
}

//переход в видовую систему координат и ортографическое проецирование 
double Ye(double x,double y,double z)
{
  return -ct*cf*x-ct*sf*y+st*z;
}


//переход от видовых координат к экранным координатам 

//переход от координты x к пикселю n
inline int xn(double x)
{
	return (int)((x - xe1)/(xe2 - xe1)*(ne2 - ne1)) + ne1;
}


//переход от координты y к пикселю m
inline int ym(double y)
{
	return (int)((y - ye1)/(ye2 - ye1)*(me2 - me1)) + me1;
}


//рисует одну линию поля из начальной точки PointB 
void LineField(HDC hdc,POINT3 PointB)
{

	VECTORS vect;	
		vect.x = PointB.x;
		vect.y = PointB.y;
		vect.z = PointB.z;
	
	//видовые координаты проецируемой точки
	double xe, ye;
//координаты пикселов
	int x1,y1,x2,y2;

	double dt = 0.01;
	double x, y, z, Hx, Hy, Hz, Ha;

	VECMAG mag;
	double xt1,yt1,zt1,xt2,yt2,zt2;

	do
		{
			x = vect.x;
			y = vect.y;
			z = vect.z;

			mag = magn(x,y,z);

			Hx = mag.hx;
			Hy = mag.hy;
			Hz = mag.hz;

			Ha = sqrt(Hx*Hx + Hy*Hy + Hz*Hz);

			vect.dx = Hx/Ha;
			vect.dy = Hy/Ha;
			vect.dz = Hz/Ha;


			xt1 = vect.x; yt1 = vect.y; zt1 = vect.z;
			xt2 = xt1 + vect.dx*dt;
			yt2 = yt1 + vect.dy*dt;
			zt2 = zt1 + vect.dz*dt;

			xe=Xe(xt1,yt1);
			ye=Ye(xt1,yt1,zt1);
			x1=xn(xe);
			y1=ym(ye);

			xe=Xe(xt2,yt2);
			ye=Ye(xt2,yt2,zt2);
			x2=xn(xe);
			y2=ym(ye);

			MoveToEx(hdc,x1,y1,NULL);
			LineTo(hdc,x2,y2);

			vect.x = xt2;
			vect.y = yt2;
			vect.z = zt2;


		}while((x>-xmax)&&(x<xmax)&&(y>-ymax)&&(y<ymax)&&(z>-zmax)&&(z<zmax));
}




//рисуем картину линий поля, координтные оис, куб и т.д.
void LinePaint(HWND hwnd)
{

//связываем размеры поля вывода с размерами клиентской области окна
//--------------------------------------------------------------------
	RECT rct;
	GetClientRect(hwnd,&rct);

	ne1 = rct.left+50; ne2 = rct.right -50;
	me1 = rct.bottom -50; me2 = rct.top + 50;
//------------------------------------------------------------------

	PAINTSTRUCT ps;

//получаем контест устройства для экрана
	HDC hdcWin = BeginPaint(hwnd, &ps);

	HDC hdc = CreateCompatibleDC(hdcWin); //создаем контекст
                     //памяти связаный с контекстом экрана

   //памяти надо придать вид экрана - подходт битовая карта с форматом
   // как у экрана. В памяти будем рисовать на битовой карте
	HBITMAP hBitmap, hBitmapOld;
	hBitmap = CreateCompatibleBitmap(hdcWin, ne2, me1); //создаем
               //битовую карту совместмую с контекстом экрана
	hBitmapOld = (HBITMAP)SelectObject(hdc, hBitmap); //помещаем
                // битовую карту в контекст памяти


//создание прямоугольной области
	HRGN hrgn2 = CreateRectRgn(ne1,me2-30,ne2,me1);

//заливаем выделенную область светлосерым цветом
	HBRUSH hBrush2 = CreateSolidBrush(RGB(0xC0,0xC0,0xC0));
    FillRgn(hdc,hrgn2,hBrush2);


	
	HPEN hPen, hPenOld;

	MoveToEx(hdc,ne1,me1-1,NULL);
	LineTo(hdc,ne2-1,me1-1);
	LineTo(hdc,ne2-1,me2);
	LineTo(hdc,ne1,me2);
	LineTo(hdc,ne1,me1);


//вычисление угловых коэффициентов поворота системы координат
	sf=sin(M_PI*angl.fi/180);
	cf=cos(M_PI*angl.fi/180);
	st=sin(M_PI*angl.teta/180);
	ct=cos(M_PI*angl.teta/180);


//информация об углах поворота системы координат
	TCHAR ss[20];
	SetBkColor(hdc,RGB(0xC0,0xC0,0xC0));
	SetTextColor(hdc,RGB(0,0,0x80));
	swprintf_s(ss,20,L"fi = %4.0lf",angl.fi);
	TextOut(hdc,(ne1+ne2)/2-80,me2-25,ss,9);
	swprintf_s(ss,20,L"teta = %4.0lf",angl.teta);
	TextOut(hdc,(ne1+ne2)/2+20,me2-25,ss,11);


//------------------------------------------------------------------------
//рисуем координтные оси
	hPen = CreatePen(PS_SOLID,1,RGB(0,255,255));
	hPenOld = SelectPen(hdc,hPen);    

//видовые координаты проецируемой точки
	double xe, ye;
//координаты пикселов
	int x1,y1,x2,y2;


//ось Ox
	xe=Xe(-xmax/3,0);
	ye=Ye(-xmax/3,0,0);
	x1=xn(xe);
	y1=ym(ye);
	xe=Xe(xmax,0);
	ye=Ye(xmax,0,0);
	x2=xn(xe);
	y2=ym(ye);
	
	MoveToEx(hdc,x1,y1,NULL);
	LineTo(hdc,x2,y2);

	SetBkColor(hdc,RGB(0xC0,0xC0,0xC0));
	SetTextColor(hdc,RGB(120,120,120));
	TextOut(hdc,x2, y2, _T("X"),1);

//Ось Oy
	xe=Xe(0,-ymax/3);
	ye=Ye(0,-ymax/3,0);
	x1=xn(xe);
	y1=ym(ye);
	xe=Xe(0,ymax);
	ye=Ye(0,ymax,0);
	x2=xn(xe);
	y2=ym(ye);
	
	MoveToEx(hdc,x1,y1,NULL);
	LineTo(hdc,x2,y2);

	SetBkColor(hdc,RGB(0xC0,0xC0,0xC0));
	SetTextColor(hdc,RGB(120,120,120));
	TextOut(hdc,x2, y2, _T("Y"),1);

//Ось Oz
	xe=Xe(0,0);
	ye=Ye(0,0,-zmax/3);
	x1=xn(xe);
	y1=ym(ye);
	xe=Xe(0,0);
	ye=Ye(0,0,zmax);
	x2=xn(xe);
	y2=ym(ye);

	MoveToEx(hdc,x1,y1,NULL);
	LineTo(hdc,x2,y2);

	SetBkColor(hdc,RGB(0xC0,0xC0,0xC0));
	SetTextColor(hdc,RGB(120,120,120));
	TextOut(hdc,x2, y2, _T("Z"),1);

	SelectPen(hdc,hPenOld);    
	DeletePen(hPen);           
//-----------------------------------------------------------------------------

//---------------------------------------------------------------------------
//рисуем магнитную пластнику желтым цветом, толщиной 4 пикселя
	hPen = CreatePen(PS_SOLID,4,RGB(255,255,0));
	hPenOld = SelectPen(hdc,hPen);    

	double xt1,yt1,zt1,xt2,yt2,zt2;
	int j;

	for(int i=0; i<4; i++)
	{
		j = i + 1;
		if(j==4)
			j = 0;
		xt1 = Px[i]; yt1 = Py[i]; zt1 = Pz[i];
		xt2 = Px[j]; yt2 = Py[j]; zt2 = Pz[j];

		xe=Xe(xt1,yt1);
		ye=Ye(xt1,yt1,zt1);
		x1=xn(xe);
		y1=ym(ye);

		xe=Xe(xt2,yt2);
		ye=Ye(xt2,yt2,zt2);
		x2=xn(xe);
		y2=ym(ye);

		MoveToEx(hdc,x1,y1,NULL);
		LineTo(hdc,x2,y2);
	}


	SelectPen(hdc,hPenOld);    
	DeletePen(hPen);           
//------------------------------------------------------------------






//----------------------------------------------------------------
//рисуем линии поля

//рисуем 16 линий поля красным цветом
	hPen = CreatePen(PS_SOLID,2,RGB(255,0,0));
	hPenOld = SelectPen(hdc,hPen);   

	for(int i=0; i<16; i++)
	{
		LineField(hdc,PointB[i]);
		
	}

	SelectPen(hdc,hPenOld);   
	DeletePen(hPen);          


//рисуем 16 линий поля синим цветом
	hPen = CreatePen(PS_SOLID,2,RGB(0,0,255));
	hPenOld = SelectPen(hdc,hPen);    

	for(int i=16; i<32; i++)
	{
		LineField(hdc,PointB[i]);
	}

	SelectPen(hdc,hPenOld);    
	DeletePen(hPen);           
//-----------------------------------------------------------------------


//----------------------------------------------------------------------
//рисуем куб
	hPen = CreatePen(PS_SOLID,1,RGB(160,160,160));
	hPenOld = SelectPen(hdc,hPen);

	DrawBox(hwnd, hdc, angl);

	SelectPen(hdc,hPenOld);
	DeletePen(hPen);       
//------------------------------------------------------------------------

	BitBlt(hdcWin,ne1,me2-30,ne2,me1,hdc,ne1,me2-30,SRCCOPY); //копи-
   //руем контекст памяти в контекст экрана

	DeleteObject(hBrush2);
	DeleteObject(hrgn2);


	SelectObject(hdc, hBitmapOld); //востанавливаем контекст памяти
	DeleteObject(hBitmap); //убираем битовую карту
	DeleteDC(hdc);  //  освобождаем контекст памяти


	EndPaint(hwnd, &ps);   
}



//обрабатывает нажатие левой клавиши мышки
void LineLButtonDown(HWND hwnd, int x, int y)
{
	Dat.ButtonDown = TRUE;
	Dat.Drawing = FALSE;
	
	anglOld.fi = angl.fi;
	anglOld.teta = angl.teta;
	corOld.x = x;
	corOld.y = y;
	
//при нажатии клавиши мыши выделяется куб синим цветом
	HDC PaintDC = GetDC(hwnd);
	HPEN hPen, hPenOld;
	hPen = CreatePen(PS_SOLID,1,RGB(0,0,255));
	hPenOld = SelectPen(PaintDC,hPen);   

	SetROP2(PaintDC, R2_NOTXORPEN);
		
	DrawBox(hwnd, PaintDC, anglOld);

	SelectPen(PaintDC,hPenOld);  
	DeletePen(hPen);           

	ReleaseDC(hwnd, PaintDC);
}

//обрабатывает отпускание левой клавиши мышки
void LineLButtonUp(HWND hwnd)
{
	if(Dat.ButtonDown && Dat.Drawing)
		Dat.Drawing = FALSE;

	Dat.ButtonDown = FALSE;
}


//обрабатывает движение мыши при нажатой левой клавиши
void LineMouseMove(HWND hwnd,int x, int y)
{

	if(Dat.ButtonDown)
	{
		Dat.Drawing = TRUE;

		HDC PaintDC = GetDC(hwnd);
		
//перерисовывает куб в новом положении в режиме NOTXOR
		HPEN hPen, hPenOld;
		hPen = CreatePen(PS_SOLID,1,RGB(0,0,255));
		hPenOld = SelectPen(PaintDC,hPen);  

		SetROP2(PaintDC, R2_NOTXORPEN);
		
		DrawBox(hwnd, PaintDC, anglOld);

		angl.fi += corOld.x-x;
		angl.teta += corOld.y-y;
		
		corOld.x = x; corOld.y = y;

		anglOld.fi   = angl.fi;
		anglOld.teta   = angl.teta;

		DrawBox(hwnd, PaintDC, anglOld);

		SelectPen(PaintDC,hPenOld);   
		DeletePen(hPen);           


//информация об углах поворота куба
		TCHAR ss[20];
		SetBkColor(PaintDC,RGB(0xC0,0xC0,0xC0));
		SetTextColor(PaintDC,RGB(0,0,0x80));
		swprintf_s(ss,20,L"fi = %4.0lf",angl.fi);
		TextOut(PaintDC,(ne1+ne2)/2-80,me2-25,ss,9);
		swprintf_s(ss,20,L"teta = %4.0lf",angl.teta);
		TextOut(PaintDC,(ne1+ne2)/2+20,me2-25,ss,11);

		ReleaseDC(hwnd, PaintDC);
	}

}


//рисуем куб, связанный с подвижной системой координат
void DrawBox(HWND hwnd, HDC hdc, ANGLS an)
{
	sf=sin(M_PI*an.fi/180);
	cf=cos(M_PI*an.fi/180);
	st=sin(M_PI*an.teta/180);
	ct=cos(M_PI*an.teta/180);

	double xe, ye;
	int x1,y1,x2,y2;
	double xt1,yt1,zt1,xt2,yt2,zt2;
	int j;

	for(int i=0; i<4; i++)
	{
		j = i + 1;
		if(j==4)
			j = 0;
		xt1 = Point[i].x; yt1 = Point[i].y; zt1 = Point[i].z;
		xt2 = Point[j].x; yt2 = Point[j].y; zt2 = Point[j].z;

		xe=Xe(xt1,yt1);
		ye=Ye(xt1,yt1,zt1);
		x1=xn(xe);
		y1=ym(ye);

		xe=Xe(xt2,yt2);
		ye=Ye(xt2,yt2,zt2);
		x2=xn(xe);
		y2=ym(ye);

		MoveToEx(hdc,x1,y1,NULL);
		LineTo(hdc,x2,y2);
	}



	for(int i=4; i<8; i++)
	{
		j = i + 1;
		if(j==8)
			j = 4;
		xt1 = Point[i].x; yt1 = Point[i].y; zt1 = Point[i].z;
		xt2 = Point[j].x; yt2 = Point[j].y; zt2 = Point[j].z;

		xe=Xe(xt1,yt1);
		ye=Ye(xt1,yt1,zt1);
		x1=xn(xe);
		y1=ym(ye);

		xe=Xe(xt2,yt2);
		ye=Ye(xt2,yt2,zt2);
		x2=xn(xe);
		y2=ym(ye);

		MoveToEx(hdc,x1,y1,NULL);
		LineTo(hdc,x2,y2);
	}

	for(int i=0; i<4; i++)
	{
		xt1 =   Point[i].x; yt1 =   Point[i].y; zt1 =   Point[i].z;
		xt2 = Point[i+4].x; yt2 = Point[i+4].y; zt2 = Point[i+4].z;

		xe=Xe(xt1,yt1);
		ye=Ye(xt1,yt1,zt1);
		x1=xn(xe);
		y1=ym(ye);

		xe=Xe(xt2,yt2);
		ye=Ye(xt2,yt2,zt2);
		x2=xn(xe);
		y2=ym(ye);

		MoveToEx(hdc,x1,y1,NULL);
		LineTo(hdc,x2,y2);
	}


	for(int i=0; i<2; i++)
	{
		xt1 =   Point[i].x; yt1 =   Point[i].y; zt1 =   Point[i].z;
		xt2 = Point[i+2].x; yt2 = Point[i+2].y; zt2 = Point[i+2].z;

		xe=Xe(xt1,yt1);
		ye=Ye(xt1,yt1,zt1);
		x1=xn(xe);
		y1=ym(ye);

		xe=Xe(xt2,yt2);
		ye=Ye(xt2,yt2,zt2);
		x2=xn(xe);
		y2=ym(ye);

		MoveToEx(hdc,x1,y1,NULL);
		LineTo(hdc,x2,y2);
	}


}



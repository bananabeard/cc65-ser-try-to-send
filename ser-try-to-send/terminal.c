/*
** Minimalistic terminal program.
**
** Makes use of the serial drivers.
**
** 2022-12-23, Oliver Schmidt (ol.sc@web.de)
**
*/



#include <cc65.h>
#include <conio.h>
#include <stdio.h>
#include <stdlib.h>
#include <serial.h>


static void check (const char* msg, unsigned char err)
{
    if (err == SER_ERR_OK) {
        return;
    }

    printf ("%s:0x%02x\n", msg, err);
    if (doesclrscrafterexit ()) {
        cgetc ();
    }
    exit (1);
}


void main (void)
{
    const struct ser_params par = {
        SER_BAUD_38400,
        SER_BITS_8,
        SER_STOP_1,
        SER_PAR_NONE,
        SER_HS_HW
    };

    check ("ser_install", ser_install (ser_static_stddrv));

    check ("ser_open", ser_open (&par));

    atexit ((void (*)) ser_close);

    printf ("Serial Port: 38400-8-1-N RTS/CTS\n");

    while (1)
    {
        char chr;

        #ifdef SER_TRY_TO_SEND
        ser_ioctl(0, 0);
        #endif

        if (kbhit ())
        {
            chr = cgetc ();

            if (ser_put (chr) == SER_ERR_OK) {
                ++VIC.bordercolor;
            }
        }

        if (ser_get (&chr) == SER_ERR_OK) {
            cbm_k_chrout(chr);
        }
    }
}

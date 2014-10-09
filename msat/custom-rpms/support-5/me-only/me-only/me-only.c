/*
 * PROGRAM
 *   me-only
 * DESCRIPTION
 *   This program is used from a bash script to obtain an
 *   excusive lock in the form of a Unix domain socket. If
 *   the Unix domain socket with the same path is already in
 *   use, it returns with an error. Some other errors may
 *   occur, but generally this program returns with success
 *   if no other program is using the same Unix domain
 *   socket.
 *
 *   We use this method in scripting because, if the script
 *   fails after obtaining this lock (Unix domain socket),
 *   the kernel removes it.
 * DEPENDENCIES
 * SOURCE FILE
 *   me-only.c
 *
 *   Compile with:
 *   $ gcc -Wall -o me-only me-only.c
 * HEADER FILE
 *   Not applicable.
 * AUTHORS
 * HISTORY
 * LICENSE
 *   Copyright (C) 2012 Allard Berends
 *   Copyright (C) 2013 Allard Berends
 * 
 *   me-only is free software; you can redistribute it
 *   and/or modify it under the terms of the GNU General
 *   Public License as published by the Free Software
 *   Foundation; either version 3 of the License, or (at
 *   your option) any later version.
 *
 *   me-only is distributed in the hope that it will be
 *   useful, but WITHOUT ANY WARRANTY; without even the
 *   implied warranty of MERCHANTABILITY or FITNESS FOR A
 *   PARTICULAR PURPOSE. See the GNU General Public License
 *   for more details.
 *
 *   You should have received a copy of the GNU General
 *   Public License along with this program; if not, write
 *   to the Free Software Foundation, Inc., 59 Temple Place
 *   - Suite 330, Boston, MA 02111-1307, USA.
 * DESIGN
 */

/*
 * Section: ansi C includes.
 */
#include <stdio.h>              /* Needed for
                                   printf,
                                   fprintf.
                                   */
#include <errno.h>              /* Needed for
                                   errno,
                                   EINTR. */
#include <string.h>             /* Needed for
                                   strlen, strncpy. */
#include <stdlib.h>             /* Needed for
                                   system. */

/*
 * Section: POSIX includes.
 */
#include <unistd.h>             /* Needed for
                                   execvp. */
#include <sys/types.h>          /* Needed for
                                   AF_INET,
                                   SOCK_STREAM. */
#include <sys/socket.h>         /* Needed for
                                   socket,
                                   bind. */
#include <sys/un.h>             /* Needed for
                                   struct sockaddr_un. */

/* UNIX_PATH_MAX is not defined in sys/un.h */
struct sockaddr_un sizecheck;
#ifndef UNIX_PATH_MAX
#define UNIX_PATH_MAX sizeof(sizecheck.sun_path)
#endif

/*
 * Section: operating system specific includes.
 */

/*
 * Section: local includes.
 */

/*
 * Section: program constant macros.
 */

/*
 * Section: program constant enumerations.
 */
/*
 * Return values of the function calls.
 * Note that the value of success must be 0 and the value of
 * failure must be 1. So success and failure should always
 * be the first 2 members of the return values enumeration.
 */
enum
{
    ME_ONLY_K_SUCCESS,              /* Must be 0! */
    ME_ONLY_K_FAILURE,              /* Must be 1! */
    ME_ONLY_K_INV_PRE_COND,         /* Invalid pre condition
                                       (input domain). */
    ME_ONLY_K_SOCKET_ERROR,         /* Error in socket function
                                       call. */
    ME_ONLY_K_BIND_ERROR,           /* Error in bind function
                                       call. */
    ME_ONLY_K_LAST
};


/*
 * Section: program function macros.
 */
#define min(a,b)    ((a) < (b) ? (a) : (b))
#define max(a,b)    ((a) > (b) ? (a) : (b))

/*
 * Section: program type definitions.
 */

/*
 * TCP server thread control structure.
 */

/*
 * Section: program static function prototypes.
 */

/*
 * Section: global variable definitions.
 */

/*
 * Section: program variable definitions.
 */

/*
 * Section: function definitions.
 */

/*
 * FUNCTION NAME
 *   main
 * FUNCTIONAL DESCRIPTION
 * FORMAL PARAMETERS
 *   argc: number of command line arguments.
 *   argv: command line arguments as strings.
 * RETURN VALUE
 *   0: success.
 *   1: failure.
 *   2: Invalid input domain.
 *   3: socket function call error.
 *   4: bind function call error.
 * SIDE EFFECTS
 * DESIGN
 */
int main(int argc, char *argv[]) {
  char                *pc_func_name              = "main";
  int                  i_ret                     = 0;
  int                  i_unix_socket             = 0;
  struct sockaddr_un   r_unix_domain_socket_path = {0};
  char               **ppc_new_argv              = NULL;
  int                  i                         = 0;

#ifdef ME_ONLY_DEBUG
  printf("Entered function %s.\n", pc_func_name);
#endif

  /*
   * Preliminary check for "-h" as first argument.
   */
  if(argc == 2 && strncmp(argv[1], "-h", 2) == 0) {
    printf("Usage:\n"
      "%s <path> <script> [arg1 [arg2 .. arg2]]\n",
      argv[0]);
    printf("For example:\n");
    printf("%s /tmp/me-only-xxy ./my-pid.sh 30\n",
      argv[0]);
    return ME_ONLY_K_SUCCESS;
  }
  /*
   * Check the input domain:
   * * We expect 1 argument
   * * Argument must be a pathname
   * * Directories in path must exist
   * * Both absolute and relative paths are ok
   */
  if(argc < 3) {
    fprintf(stderr,
            "File %s, function %s, "
            "error at line %d.\n"
            "Need socket path and path of command to execute.\n",
            __FILE__,
            pc_func_name,
            __LINE__);
    return ME_ONLY_K_INV_PRE_COND;
  }

  i_unix_socket = socket(AF_UNIX, SOCK_STREAM, 0);
  if(i_unix_socket == -1) {
    fprintf(stderr,
            "File %s, function %s, "
            "error at line %d.\n"
            "%s\n",
            __FILE__,
            pc_func_name,
            __LINE__,
            strerror(errno));
    return ME_ONLY_K_SOCKET_ERROR;
  }

  r_unix_domain_socket_path.sun_family = AF_UNIX;
  (void) strncpy(r_unix_domain_socket_path.sun_path + 1, argv[1], sizeof(r_unix_domain_socket_path.sun_path - 2));
  i_ret = bind(i_unix_socket, (struct sockaddr *) &r_unix_domain_socket_path, sizeof(struct sockaddr_un));
  if(i_ret == -1) {
    fprintf(stderr,
            "File %s, function %s, "
            "error at line %d.\n"
            "%s\n",
            __FILE__,
            pc_func_name,
            __LINE__,
            strerror(errno));
    return ME_ONLY_K_BIND_ERROR;
  }

  ppc_new_argv = malloc((argc - 1) * sizeof(char *));
  for(i = 0; i < argc - 1; i++) {
    ppc_new_argv[i] = argv[i + 2];
  }
  ppc_new_argv[argc - 2] = NULL;
  i_ret = execv(argv[2], ppc_new_argv);
  if(i_ret == -1) {
    fprintf(stderr,
            "File %s, function %s, "
            "error at line %d.\n"
            "%s\n",
            __FILE__,
            pc_func_name,
            __LINE__,
            strerror(errno));
    return ME_ONLY_K_FAILURE;
  }

  return ME_ONLY_K_SUCCESS;
} /* End of main. */


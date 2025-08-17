import sys
import xmlrpc.client

SUPERVISOR_URL = "http://localhost:9005/RPC2"

if __name__ == "__main__":
    try:
        server = xmlrpc.client.ServerProxy(SUPERVISOR_URL)

        all_processes_info = server.supervisor.getAllProcessInfo()

        error_processes = []
        for proc in all_processes_info:
            if proc['state'] != 20:
                error_processes.append(f"  - Proses '{proc['name']}' dalam status '{proc['statename']}'")

        if error_processes:
            print("Health check GAGAL. Proses berikut tidak berjalan dengan benar:")
            for error in error_processes:
                print(error)
            sys.exit(1)

        else:
            print("Health check BERHASIL. Semua proses dalam status 'RUNNING'.")
            sys.exit(0)

    except ConnectionRefusedError:
        print("Health check GAGAL: Koneksi ke SupervisorD ditolak. Layanan mungkin belum siap.")
        sys.exit(1)

    except Exception as e:
        print(f"Health check GAGAL: Terjadi error tak terduga -> {e}")
        sys.exit(1)
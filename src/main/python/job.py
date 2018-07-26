from db.dbutil import *
from datetime import datetime


class Job:
    """
    An object representing an entry in the job table.
    """

    def __init__(self, job_type):
        self.id = None
        self.job_type = job_type
        self.start_time = datetime.now()
        self.end_time = None
        self.status = 'STARTED'
        self.progress = 0

    def __str__(self):
        s = "id = " + str(self.id) + ", "
        s += "job_type = " + self.job_type + ", "
        s += "status = " + self.status + ", "
        s += "start_time = " + str(self.start_time) + ", "
        s += "end_time = " + str(self.end_time) + ", "
        return s

    def start(self):
        conn = get_conn()
        c = conn.cursor()
        res = c.execute('INSERT INTO JOB(JOB_TYPE, START_TIME, STATUS, PROGRESS) values (?, ?, ?, ?)',
                        (self.job_type, self.start_time, self.status, self.progress))
        print('Created Job Id -> ' + str(c.lastrowid))
        self.id = c.lastrowid
        conn.commit()

        close_conn(conn)

    def update_progress(self, progress_val):
        self.progress = progress_val

        conn = get_conn()
        c = conn.cursor()
        res = c.execute('UPDATE JOB SET PROGRESS=? WHERE JOB_ID=?',
                        (self.progress, self.id))
        conn.commit()
        close_conn(conn)

    def finish(self, status):
        self.end_time = datetime.now()
        self.status = status
        if status == 'COMPLETED':
            self.progress = 100.0

        conn = get_conn()
        c = conn.cursor()
        res = c.execute('UPDATE JOB SET END_TIME=?, STATUS=?, PROGRESS=? WHERE JOB_ID=?',
                        (self.end_time, self.status, self.progress, self.id))
        conn.commit()
        close_conn(conn)


if __name__ == "__main__":
    j = Job('dummy')
    j.start()
    j.update_progress(25.0)
    j.update_progress(75.0)
    j.finish('COMPLETED')

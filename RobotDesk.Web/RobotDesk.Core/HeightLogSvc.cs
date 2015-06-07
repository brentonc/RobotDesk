using System;
using System.Collections.Generic;
using System.Linq;
using RobotDesk.Core.Data;

namespace RobotDesk.Core {
    public class HeightLogSvc {
        public void SaveHeightLogEntry(HeightLog entry) {

            if (entry == null) throw new ArgumentNullException();
            if (string.IsNullOrEmpty(entry.id)) {
                entry.id = Guid.NewGuid().ToString();
            }
            using (var dbContext = new RobotDeskData()) {
                dbContext.HeightLogs.Add(entry);
                dbContext.SaveChanges();
            }
        }

        public HeightLog GetCurrentHeight() {

            using (var dbContext = new RobotDeskData()) {
                var q = from ht in dbContext.HeightLogs
                    orderby ht.move_initiate_time descending
                    select ht;
                return q.FirstOrDefault();
            }
        }
//
//        public List<HeightLog> GetRecentHeightLogs() {
//            return GetRecentHeightLogs(new TimeSpan(24, 0, 0));
//        }
//
//        public List<HeightLog> GetRecentHeightLogs(TimeSpan ts) {
//            using (var dbContext = new RobotDeskData()) {
//                var q = from ht in dbContext.HeightLogs
//                    orderby ht.move_initiate_time
//                    where ht.move_initiate_time > DateTime.Now.Subtract(ts)
//                    select ht;
//
//                return q.ToList<HeightLog>();
//            }
//        }

        public List<HeightLog> GetRecentHeightLogs(int count) {
            using (var dbContext = new RobotDeskData()) {
                var q = from ht in dbContext.HeightLogs
                    orderby ht.move_initiate_time descending
                    select ht;

                return q.Take(count).ToList<HeightLog>();
            }
        }
    }
}

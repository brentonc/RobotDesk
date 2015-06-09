using System;
using System.Collections.Generic;
using System.Linq;
using RobotDesk.Core.Data;

namespace RobotDesk.Core {
    public class HeightLogSvc {

        /// <summary>
        /// Saves a height entry to the database
        /// </summary>
        /// <param name="entry"></param>
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

        /// <summary>
        /// Gets the most recent height entry
        /// </summary>
        /// <returns></returns>
        public HeightLog GetCurrentHeight() {

            using (var dbContext = new RobotDeskData()) {
                var q = from ht in dbContext.HeightLogs
                    orderby ht.move_initiate_time descending
                    select ht;
                return q.FirstOrDefault();
            }
        }

        /// <summary>
        /// Gets the n most recent log entries
        /// </summary>
        /// <param name="count"></param>
        /// <returns></returns>
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

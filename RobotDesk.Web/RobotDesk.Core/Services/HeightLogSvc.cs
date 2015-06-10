using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using RobotDesk.Core.Data;

namespace RobotDesk.Core.Services {
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

        /// <summary>
        /// Provides the records from the specified period, as well as the one precending.  This allows consumers to see whether the desk 
        /// was previously in a sit or stand mode.
        /// </summary>
        /// <param name="periodStart"></param>
        /// <param name="periodEnd"></param>
        /// <returns></returns>
        public List<HeightLog> GetPeriodHeightLogsPlusOneMore(DateTime periodStart, DateTime periodEnd) {
            using (var dbContext = new RobotDeskData()) {
                var q = (from ht in dbContext.HeightLogs
                    where ht.move_initiate_time >= periodStart && ht.move_initiate_time <= periodEnd
                    orderby ht.move_initiate_time descending
                    select ht).Concat(
                        (from ht in dbContext.HeightLogs
                            where ht.move_initiate_time <= periodStart
                            orderby ht.move_initiate_time descending
                            select ht).Take(1)
                    );

                return q.ToList<HeightLog>();

            }
        }
    }
}

using System;
using System.Collections.Generic;
using RobotDesk.Core.Data;

namespace RobotDesk.Core
{
    public class HeightLogSvc
    {
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

//        public HeightLog GetCurrentHeight() {
//            
//            using (var dbContext = new RobotDeskData())
//            {
//
//            }
//                
//        }

        public List<HeightLog> GetRecentHeightLogs() {
            throw new NotImplementedException();
        }

        public List<HeightLog> GetRecentHeightLogs(TimeSpan ts) {
            throw new NotImplementedException();
        } 


    }
}

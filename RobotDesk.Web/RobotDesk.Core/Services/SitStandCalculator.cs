using System;
using System.Collections.Generic;

namespace RobotDesk.Core.Services
{
    public class SitStandCalculator
    {
        public StandResult Calculate(IList<SitStandCalculator> logEntries) {
            return null;
        }
    }

    public class StandResult
    {
        public float StandMinutes { get; set; }

        public float SitMinutes { get; set; }  

        public DateTime PeriodStart { get; set; }

        public DateTime PeriodEnd { get; set; }
    }
    
}

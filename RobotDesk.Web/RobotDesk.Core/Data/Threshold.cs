namespace RobotDesk.Core.Data
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("Threshold")]
    public partial class Threshold
    {
        public int id { get; set; }

        public double? range_lower_bound { get; set; }

        public double? range_upper_bound { get; set; }

        public bool is_standing { get; set; }
    }
}

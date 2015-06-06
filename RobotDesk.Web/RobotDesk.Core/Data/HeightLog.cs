namespace RobotDesk.Core.Data
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("HeightLog")]
    public partial class HeightLog
    {
        public string id { get; set; }

        [Required]
        [StringLength(100)]
        public string device_id { get; set; }

        [StringLength(100)]
        public string command_text { get; set; }

        public double? from_height { get; set; }

        public double? to_height { get; set; }

        public double? move_duration_seconds { get; set; }

        public DateTime? move_initiate_time { get; set; }
    }
}

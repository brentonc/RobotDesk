namespace RobotDesk.Core.Data
{
    using System;
    using System.Data.Entity;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Linq;

    public partial class RobotDeskData : DbContext
    {
        public RobotDeskData()
            : base("name=RobotDeskData")
        {
        }

        public virtual DbSet<HeightLog> HeightLogs { get; set; }
        public virtual DbSet<Threshold> Thresholds { get; set; }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            modelBuilder.Entity<HeightLog>()
                .Property(e => e.device_id)
                .IsUnicode(false);
        }
    }
}

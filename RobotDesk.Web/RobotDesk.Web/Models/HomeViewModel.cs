using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using RobotDesk.Core.Data;

namespace RobotDesk.Web.Models
{
    public class HomeViewModel
    {
        public List<HeightLog> Log { get; set; }
        public HeightLog CurrentHeight { get; set; }
    }
}
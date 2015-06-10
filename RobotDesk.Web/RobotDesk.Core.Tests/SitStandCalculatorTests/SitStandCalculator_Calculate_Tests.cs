using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using RobotDesk.Core.Services;

namespace RobotDesk.Core.Tests.SitStandCalculatorTests
{
    [TestClass]
    public class SitStandCalculator_Calculate_Tests
    {

        [TestMethod]
        public void can_be_run_in_test_harness() {
            //ARRANGE
            var sut = new SitStandCalculator();

            //ACT
            var result = sut.Calculate(null);

            //ASSERT
            //no-op
        }

    }
}

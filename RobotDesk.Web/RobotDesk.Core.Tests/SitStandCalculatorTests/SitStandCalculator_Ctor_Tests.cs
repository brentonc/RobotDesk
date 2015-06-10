using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using RobotDesk.Core.Services;

namespace RobotDesk.Core.Tests.SitStandCalculatorTests
{
    [TestClass]
    public class SitStandCalculator_Ctor_Tests
    {

        [TestMethod]
        public void when_calculator_created_then_readytocalc() {
            //ARRANGE
            
            //ACT
            var sut = new SitStandCalculator();

            //ASSERT
            Assert.IsNotNull(sut);
        }


    }
}

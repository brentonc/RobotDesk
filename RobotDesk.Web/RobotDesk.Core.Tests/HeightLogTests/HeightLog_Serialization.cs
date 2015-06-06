using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Newtonsoft.Json;
using RobotDesk.Core.Data;

namespace RobotDesk.Core.Tests.HeightLogTests
{
    [TestClass]
    public class HeightLog_Serialization
    {
        [TestMethod]
        public void when_jsonserialized_then_jsonisasexpected() {
            //ARRANGE
            var ht = new HeightLog {
                command_text = "Test Command",
                device_id = "Test Device",
                from_height = 0.0,
                to_height = 15.5,
                move_duration_seconds = 4.2,
                move_initiate_time = new DateTime(2015,6,6,4,3,2)
            };

            //ACT
            string output = JsonConvert.SerializeObject(ht);
            Console.WriteLine(output);

            //ASSERT
            var ht2 = JsonConvert.DeserializeObject<HeightLog>(output);
            Assert.AreEqual(ht.command_text, ht2.command_text);
            Assert.AreEqual(ht.device_id, ht2.device_id);
            Assert.AreEqual(ht.from_height, ht2.from_height);
            Assert.AreEqual(ht.to_height, ht2.to_height);
            Assert.AreEqual(ht.move_duration_seconds, ht2.move_duration_seconds);
            Assert.AreEqual(ht.move_initiate_time, ht2.move_initiate_time);
        }


    }
}

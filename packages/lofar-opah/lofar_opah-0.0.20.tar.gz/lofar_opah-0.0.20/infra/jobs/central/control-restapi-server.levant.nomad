job "control-restapi-server" {
  datacenters = ["nl-north"]
  type        = "service"
  reschedule {
    unlimited      = true
    delay          = "30s"
    delay_function = "constant"
  }
  group "control-restapi-server" {
    network {
      mode = "bridge"

      port "restapi" {
        static = "50053"
      }

      port "metrics" {
        to = "8002"
      }
    }

    service {
      name = "controlrestapi"
      port = "restapi"
    }

    service {
      tags = ["scrape"]
      name = "controlrestapi-metrics"
      port = "metrics"

      meta {
        metrics_path = "/"
      }
    }

    task "control-restapi-server"{
      driver = "docker"

      config {
        image      = "git.astron.nl:5000/lofar2.0/opah/opah:[[ $.image_tag ]]"
        entrypoint = [""]
        command    = "l2ss-opah-control-restapi-server"
        args       = [
          "--port", "${NOMAD_PORT_restapi}",
          "--metrics-port", "${NOMAD_PORT_metrics}",
          "--stationsuffix", "c.control.lofar"
        ]
      }

      resources {
        cpu    = 25
        memory = 512
      }
    }
  }
}

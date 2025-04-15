job "control-restapi" {
  datacenters = ["stat"]
  type        = "service"
  reschedule {
    unlimited      = true
    delay          = "30s"
    delay_function = "constant"
  }
  group "control-restapi" {
    network {
      mode = "bridge"

      port "restapi" {
        static       = "50053"
        host_network = "external"
      }

      port "metrics" {
        to           = "8002"
        host_network = "station"
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
          "--remote-grpc-host", "rpc.service.consul",
          "--stationsuffix", ""
        ]
      }

      resources {
        cpu    = 25
        memory = 512
      }
    }
  }
}
